# 📚 BookVerse — Online Book Store

A full-stack Django web application for browsing and purchasing books, featuring AI-powered summaries via Google Gemini.

## 🚀 Quick Setup (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Enter: username, email, password

### 4. Populate Sample Data
```bash
python manage.py populate_data
```
This adds 10 categories and 20 sample books.

### 5. Start the Server
```bash
python manage.py runserver
```

### 6. Open in Browser
- 🌐 Website: http://127.0.0.1:8000/
- 🔧 Admin Panel: http://127.0.0.1:8000/admin/

---

## 🤖 Google Gemini AI Setup (Optional)

1. Go to https://aistudio.google.com/app/apikey
2. Create a free API key
3. Open `bookstore/settings.py`
4. Replace `'YOUR_GEMINI_API_KEY_HERE'` with your key:
   ```python
   GEMINI_API_KEY = 'your-actual-key-here'
   ```

Without the key, a demo summary is generated automatically.

---

## 📁 Project Structure

```
bookstore/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3              (created after migrate)
├── bookstore/
│   ├── settings.py         ← Configure GEMINI_API_KEY here
│   ├── urls.py
│   └── wsgi.py
├── store/
│   ├── models.py           ← Database models
│   ├── views.py            ← Page logic
│   ├── urls.py             ← URL routing
│   ├── admin.py            ← Admin panel config
│   ├── context_processors.py
│   ├── templates/store/    ← All HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── book_list.html
│   │   ├── book_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_success.html
│   │   ├── search_results.html
│   │   ├── category_books.html
│   │   └── partials/
│   │       └── book_card.html
│   └── management/commands/
│       └── populate_data.py ← Sample data seeder
├── static/                 ← CSS, JS, Images
└── media/                  ← Uploaded book covers
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 Homepage | Hero banner, featured books, categories |
| 📚 Book Listing | Filter by category, sort, book type |
| 📖 Book Detail | Full info, reviews, AI summary |
| 🏆 Bestsellers | Top-rated/most-sold books |
| 🆕 New Arrivals | Recently added books |
| 🎧 Audiobooks | Audio format books |
| 🔍 Search | Search by title, author, category |
| 🛒 Cart | Add/remove/update quantities |
| 💳 Checkout | Shipping form + payment selection |
| ✅ Order Success | Confirmation with order number |
| 📧 Newsletter | Email subscription |
| ⭐ Reviews | Submit and view book reviews |
| 🤖 AI Summary | Google Gemini book summaries |
| 🔧 Admin Panel | Full CRUD for all models |

---

## 🔧 Admin Panel Guide

Visit http://127.0.0.1:8000/admin/

### Adding Books:
1. First add **Categories** (with emoji icons)
2. Then add **Books** — mark as Bestseller/New Arrival/Featured
3. Upload cover images (optional but recommended)

### Managing Orders:
- View all orders with customer details
- Update order status (pending → confirmed → shipped → delivered)

### Newsletter Subscribers:
- View all subscribed emails
- Export list from admin

---

## 🛠️ VSCode Setup Tips

1. Install extension: **Python** (ms-python.python)
2. Install extension: **Django** (batisteo.vscode-django)
3. Set Python interpreter to your venv/system Python
4. Terminal: `python manage.py runserver`

---

## 📦 Technologies Used

- **Backend**: Python 3.x, Django 4.2+
- **Database**: SQLite (built-in)
- **Frontend**: Bootstrap 5.3, Font Awesome 6, Google Fonts
- **AI**: Google Gemini API (Generative AI)
- **Image Handling**: Pillow
