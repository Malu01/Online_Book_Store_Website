from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Book, Subscriber, Review, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'slug', 'book_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_display_links = ['name']

    def book_count(self, obj):
        count = obj.books.filter(is_active=True).count()
        return format_html('<span style="color:#2ecc71;font-weight:bold">{}</span>', count)
    book_count.short_description = 'Books'


class BookAdmin(admin.ModelAdmin):
    list_display = ['cover_preview', 'title', 'author', 'category', 'price', 'rating', 'is_bestseller', 'is_new_arrival', 'is_active', 'stock']
    list_filter = ['category', 'is_bestseller', 'is_new_arrival', 'is_featured', 'book_type', 'is_active']
    search_fields = ['title', 'author', 'isbn']
    list_editable = ['price', 'is_bestseller', 'is_new_arrival', 'is_active', 'stock']
    list_display_links = ['title']
    readonly_fields = ['ai_summary', 'cover_preview_large', 'created_at', 'updated_at']
    fieldsets = (
        ('📖 Book Info', {
            'fields': ('title', 'author', 'category', 'isbn', 'book_type', 'language')
        }),
        ('📝 Content', {
            'fields': ('description', 'ai_summary')
        }),
        ('🖼️ Media', {
            'fields': ('cover_image', 'cover_preview_large')
        }),
        ('💰 Pricing', {
            'fields': ('price', 'original_price', 'stock')
        }),
        ('📊 Details', {
            'fields': ('publisher', 'publication_date', 'pages', 'rating', 'review_count')
        }),
        ('⭐ Featured', {
            'fields': ('is_bestseller', 'is_new_arrival', 'is_featured', 'is_active')
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="40" height="55" style="object-fit:cover;border-radius:4px;">', obj.cover_image.url)
        return format_html('<div style="width:40px;height:55px;background:#667eea;border-radius:4px;display:flex;align-items:center;justify-content:center;color:white;font-size:16px;">📚</div>')
    cover_preview.short_description = 'Cover'

    def cover_preview_large(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="150" style="border-radius:8px;">', obj.cover_image.url)
        return "No image"
    cover_preview_large.short_description = 'Cover Preview'

admin.site.register(Book, BookAdmin)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    readonly_fields = ['subscribed_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'reviewer_name', 'rating', 'created_at', 'is_approved']
    list_filter = ['rating', 'is_approved']
    search_fields = ['reviewer_name', 'book__title']
    list_editable = ['is_approved']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['book', 'quantity', 'subtotal']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'item_count', 'total', 'created_at']
    inlines = [CartItemInline]
    readonly_fields = ['session_key', 'created_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['book', 'quantity', 'price', 'subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'total_amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'full_name', 'email']
    list_editable = ['status']
    readonly_fields = ['order_number', 'created_at']
    inlines = [OrderItemInline]
