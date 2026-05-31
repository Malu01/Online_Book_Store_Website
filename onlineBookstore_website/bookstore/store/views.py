import json
import random
import string
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q, Avg
from django.conf import settings
from django.views.decorators.http import require_POST
from .models import Book, Category, Subscriber, Cart, CartItem, Review, Order, OrderItem


def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def home(request):
    categories = Category.objects.all()
    bestsellers = Book.objects.filter(is_bestseller=True, is_active=True)[:8]
    new_arrivals = Book.objects.filter(is_new_arrival=True, is_active=True)[:8]
    featured = Book.objects.filter(is_featured=True, is_active=True)[:4]
    audiobooks = Book.objects.filter(book_type='audiobook', is_active=True)[:4]
    top_rated = Book.objects.filter(is_active=True).order_by('-rating')[:6]

    context = {
        'categories': categories,
        'bestsellers': bestsellers,
        'new_arrivals': new_arrivals,
        'featured': featured,
        'audiobooks': audiobooks,
        'top_rated': top_rated,
    }
    return render(request, 'store/home.html', context)


def book_list(request):
    books = Book.objects.filter(is_active=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    sort = request.GET.get('sort', 'newest')
    book_type = request.GET.get('type')

    if category_slug:
        books = books.filter(category__slug=category_slug)
    if book_type:
        books = books.filter(book_type=book_type)

    if sort == 'price_low':
        books = books.order_by('price')
    elif sort == 'price_high':
        books = books.order_by('-price')
    elif sort == 'rating':
        books = books.order_by('-rating')
    elif sort == 'title':
        books = books.order_by('title')
    else:
        books = books.order_by('-created_at')

    context = {
        'books': books,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort,
        'current_type': book_type,
        'total_books': books.count(),
    }
    return render(request, 'store/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, is_active=True)
    reviews = book.reviews.filter(is_approved=True)
    related_books = Book.objects.filter(
        category=book.category, is_active=True
    ).exclude(pk=pk)[:4]

    if request.method == 'POST':
        name = request.POST.get('reviewer_name')
        email = request.POST.get('reviewer_email')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if name and email and rating and comment:
            Review.objects.create(book=book, reviewer_name=name, reviewer_email=email, rating=int(rating), comment=comment)
            avg = book.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg']
            book.rating = round(avg or 0, 1)
            book.review_count = book.reviews.filter(is_approved=True).count()
            book.save()
            messages.success(request, '✅ Your review has been submitted!')
            return redirect('book_detail', pk=pk)

    context = {
        'book': book,
        'reviews': reviews,
        'related_books': related_books,
        'star_range': range(1, 6),
    }
    return render(request, 'store/book_detail.html', context)


def category_books(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category, is_active=True)
    context = {'category': category, 'books': books}
    return render(request, 'store/category_books.html', context)


def bestsellers(request):
    books = Book.objects.filter(is_bestseller=True, is_active=True)
    return render(request, 'store/book_list.html', {'books': books, 'page_title': '🏆 Best Sellers', 'total_books': books.count()})


def new_arrivals(request):
    books = Book.objects.filter(is_new_arrival=True, is_active=True)
    return render(request, 'store/book_list.html', {'books': books, 'page_title': '🆕 New Arrivals', 'total_books': books.count()})


def audiobooks(request):
    books = Book.objects.filter(book_type='audiobook', is_active=True)
    return render(request, 'store/book_list.html', {'books': books, 'page_title': '🎧 Audiobooks', 'total_books': books.count()})


def search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(is_active=True)
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    context = {'books': books, 'query': query, 'total_books': books.count()}
    return render(request, 'store/search_results.html', context)


def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id, is_active=True)
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'✅ "{book.title}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__session_key=request.session.session_key)
    item.delete()
    messages.success(request, '🗑️ Item removed from cart.')
    return redirect('cart')


@require_POST
def update_cart(request):
    cart = get_or_create_cart(request)
    for key, val in request.POST.items():
        if key.startswith('quantity_'):
            item_id = key.split('_')[1]
            try:
                item = CartItem.objects.get(pk=item_id, cart=cart)
                qty = int(val)
                if qty > 0:
                    item.quantity = qty
                    item.save()
                else:
                    item.delete()
            except (CartItem.DoesNotExist, ValueError):
                pass
    messages.success(request, '🛒 Cart updated!')
    return redirect('cart')


def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    if request.method == 'POST':
        order_number = 'BV' + ''.join(random.choices(string.digits, k=8))
        order = Order.objects.create(
            order_number=order_number,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            total_amount=cart.total,
            payment_method=request.POST.get('payment_method', 'COD'),
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity, price=item.book.price)
        cart.items.all().delete()
        return redirect('order_success', order_number=order_number)

    return render(request, 'store/checkout.html', {'cart': cart})


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'store/order_success.html', {'order': order})


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        if email:
            sub, created = Subscriber.objects.get_or_create(email=email, defaults={'name': name})
            if created:
                return JsonResponse({'status': 'success', 'message': '🎉 You\'ve successfully subscribed!'})
            else:
                return JsonResponse({'status': 'info', 'message': '📧 You\'re already subscribed!'})
    return JsonResponse({'status': 'error', 'message': '❌ Invalid request.'})


def get_ai_summary(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.ai_summary:
        return JsonResponse({'summary': book.ai_summary, 'cached': True})

    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY_HERE':
        # Fallback demo summary
        summary = f'"{book.title}" by {book.author} is a captivating {book.category.name.lower()} book that takes readers on an unforgettable journey. This {book.pages or ""}{"page" if book.pages else ""} masterpiece explores profound themes and delivers an engaging narrative that keeps readers hooked from the very first page to the last. Published by {book.publisher or "a renowned publisher"}, this book has earned its place among the must-reads in its genre.'
        book.ai_summary = summary
        book.save()
        return JsonResponse({'summary': summary, 'cached': False, 'demo': True})

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Write a compelling 3-sentence book summary for '{book.title}' by {book.author}. Category: {book.category.name}. Make it engaging and informative for potential buyers."
                }]
            }]
        }
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        summary = data['candidates'][0]['content']['parts'][0]['text']
        book.ai_summary = summary
        book.save()
        return JsonResponse({'summary': summary, 'cached': False})
    except Exception as e:
        return JsonResponse({'error': str(e), 'summary': 'Unable to fetch AI summary at this time.'}, status=200)


# ─── AUTH VIEWS ───────────────────────────────────────────────

from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        # Allow login with email too
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                pass
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            messages.success(request, f'👋 Welcome back, {user.first_name or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'store/login.html', {'next': request.GET.get('next', '')})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        pw1        = request.POST.get('password1', '')
        pw2        = request.POST.get('password2', '')
        agree      = request.POST.get('agree_terms')

        if not agree:
            messages.error(request, 'You must agree to the Terms of Service to create an account.')
        elif len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'That username is already taken. Please choose another.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists. Try logging in.')
        elif pw1 != pw2:
            messages.error(request, 'Passwords do not match.')
        elif len(pw1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=pw1,
                first_name=first_name, last_name=last_name
            )
            login(request, user)
            messages.success(request, f'🎉 Welcome to BookVerse, {first_name or username}! Your account is ready.')
            return redirect('home')
    return render(request, 'store/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request, '👋 You have been signed out. See you soon!')
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    orders = Order.objects.filter(email=user.email).order_by('-created_at')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name  = request.POST.get('last_name', '').strip()
            new_email = request.POST.get('email', '').strip()
            if new_email and new_email != user.email:
                if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                    messages.error(request, 'That email is already in use.')
                    return redirect('profile')
                user.email = new_email
            user.save()
            messages.success(request, '✅ Profile updated successfully!')

        elif form_type == 'password':
            current_pw = request.POST.get('current_password')
            new_pw1    = request.POST.get('new_password1')
            new_pw2    = request.POST.get('new_password2')
            if not user.check_password(current_pw):
                messages.error(request, '⚠️ Current password is incorrect.')
            elif new_pw1 != new_pw2:
                messages.error(request, '⚠️ New passwords do not match.')
            elif len(new_pw1) < 8:
                messages.error(request, '⚠️ Password must be at least 8 characters.')
            else:
                user.set_password(new_pw1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, '🔒 Password changed successfully!')

        return redirect('profile')

    return render(request, 'store/profile.html', {'orders': orders})
