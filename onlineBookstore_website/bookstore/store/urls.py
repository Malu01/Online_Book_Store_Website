from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('category/<slug:slug>/', views.category_books, name='category_books'),
    path('bestsellers/', views.bestsellers, name='bestsellers'),
    path('new-arrivals/', views.new_arrivals, name='new_arrivals'),
    path('audiobooks/', views.audiobooks, name='audiobooks'),
    path('search/', views.search, name='search'),
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<str:order_number>/', views.order_success, name='order_success'),
    # Newsletter
    path('subscribe/', views.subscribe, name='subscribe'),
    # AI Summary
    path('books/<int:pk>/ai-summary/', views.get_ai_summary, name='ai_summary'),
    # Auth
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
