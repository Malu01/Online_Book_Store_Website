from django.core.management.base import BaseCommand
from store.models import Category, Book
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample books and categories'

    def handle(self, *args, **options):
        # Categories
        cats_data = [
            ('Fiction', 'fiction', '✨', 'Classic and contemporary fiction'),
            ('Non-Fiction', 'non-fiction', '📰', 'Real-world facts and stories'),
            ('Science & Tech', 'science-tech', '🔬', 'Science, technology & innovation'),
            ('Self Help', 'self-help', '🌟', 'Personal growth and development'),
            ('History', 'history', '🏛️', 'Historical events and biographies'),
            ('Romance', 'romance', '❤️', 'Love stories and relationships'),
            ('Mystery & Thriller', 'mystery-thriller', '🔍', 'Suspense and detective stories'),
            ('Children', 'children', '🧸', 'Books for young readers'),
            ('Business', 'business', '💼', 'Business and entrepreneurship'),
            ('Philosophy', 'philosophy', '🧠', 'Ideas and wisdom'),
        ]
        cats = {}
        for name, slug, icon, desc in cats_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon, 'description': desc})
            cats[slug] = cat

        # Books
        books_data = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'fiction', '399', '599', 4.5, 1243, True, False, 'physical', 'A story of wealth, love, and the American Dream set in the Roaring Twenties.', 180),
            ('To Kill a Mockingbird', 'Harper Lee', 'fiction', '349', '499', 4.8, 2891, True, False, 'physical', 'A powerful story of racial injustice and moral growth in the American South.', 281),
            ('Sapiens', 'Yuval Noah Harari', 'non-fiction', '499', '799', 4.7, 5621, True, False, 'physical', 'A brief history of humankind from ancient times to modern day.', 443),
            ('Atomic Habits', 'James Clear', 'self-help', '449', '699', 4.9, 8932, True, False, 'physical', 'Tiny changes, remarkable results. A practical guide to building good habits.', 320),
            ('The Da Vinci Code', 'Dan Brown', 'mystery-thriller', '299', '449', 4.3, 3210, True, True, 'physical', 'A cryptic murder mystery involving a secret society and sacred codes.', 454),
            ('1984', 'George Orwell', 'fiction', '279', '399', 4.9, 7654, True, False, 'physical', 'A dystopian nightmare of totalitarian control and surveillance.', 328),
            ('A Brief History of Time', 'Stephen Hawking', 'science-tech', '399', '599', 4.6, 3456, False, True, 'physical', 'The cosmos explained in accessible, fascinating language.', 212),
            ('The Lean Startup', 'Eric Ries', 'business', '549', '799', 4.4, 2341, True, False, 'physical', 'How entrepreneurs use continuous innovation to create businesses.', 336),
            ('Pride and Prejudice', 'Jane Austen', 'romance', '229', '349', 4.7, 4521, False, False, 'physical', 'The timeless love story of Elizabeth Bennet and Mr. Darcy.', 279),
            ('Thinking, Fast and Slow', 'Daniel Kahneman', 'non-fiction', '599', '899', 4.5, 3122, False, True, 'physical', 'How two systems drive the way we think and make choices.', 499),
            ('Harry Potter & the Philosopher Stone', 'J.K. Rowling', 'fiction', '399', '549', 4.9, 12453, True, False, 'physical', 'A young wizard discovers his magical heritage and destiny.', 309),
            ('Dune', 'Frank Herbert', 'fiction', '449', '649', 4.7, 5432, True, True, 'physical', 'An epic science fiction saga of politics, religion, and ecology.', 688),
            ('The Psychology of Money', 'Morgan Housel', 'business', '399', '599', 4.8, 4567, True, True, 'physical', 'Timeless lessons on wealth, greed, and happiness.', 256),
            ('Becoming', 'Michelle Obama', 'non-fiction', '549', '799', 4.8, 6789, False, True, 'physical', 'An intimate memoir by the former First Lady of the United States.', 426),
            ('The Alchemist', 'Paulo Coelho', 'fiction', '299', '449', 4.6, 8901, True, False, 'physical', 'A mystical story about following your dreams and destiny.', 208),
            ('Atomic Habits Audio', 'James Clear', 'self-help', '199', '299', 4.9, 2341, True, True, 'audiobook', 'The complete audiobook narrated by the author himself.', None),
            ('Sapiens Audio', 'Yuval Noah Harari', 'non-fiction', '249', '399', 4.7, 1876, False, True, 'audiobook', 'Full audiobook version of the bestselling history of humankind.', None),
            ('The Midnight Library', 'Matt Haig', 'fiction', '349', '499', 4.5, 3241, False, True, 'physical', 'A library between life and death holds books of possible lives.', 288),
            ('Zero to One', 'Peter Thiel', 'business', '449', '649', 4.4, 2134, False, True, 'physical', 'Notes on startups, or how to build the future.', 224),
            ('The Subtle Art of Not Giving a F*ck', 'Mark Manson', 'self-help', '349', '499', 4.3, 6543, True, False, 'physical', 'A counterintuitive approach to living a good life.', 224),
        ]

        for title, author, cat_slug, price, orig, rating, reviews, bs, na, btype, desc, pages in books_data:
            Book.objects.get_or_create(
                title=title,
                defaults={
                    'author': author, 'category': cats[cat_slug],
                    'price': Decimal(price), 'original_price': Decimal(orig),
                    'rating': rating, 'review_count': reviews,
                    'is_bestseller': bs, 'is_new_arrival': na,
                    'book_type': btype, 'description': desc, 'pages': pages,
                    'is_featured': bs, 'language': 'English',
                    'publisher': 'BookVerse Publishers', 'stock': 50,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(cats_data)} categories and {len(books_data)} books!'))
        self.stdout.write(self.style.WARNING('👉 Run: python manage.py createsuperuser'))
        self.stdout.write(self.style.WARNING('👉 Then: python manage.py runserver'))
