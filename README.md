# J&N Building Products Website
### "Make Your House Smile" — Built with Django

A professional lead generation website for J&N Building Products, a construction & manufacturing company based in Malawi.

---

## 🚀 Quick Start

```bash
# 1. Clone or extract the project
cd jn_building_products

# 2. Run the setup script (does everything automatically)
chmod +x setup.sh
./setup.sh

# 3. Start the server
source venv/bin/activate
python manage.py runserver

# 4. Open in browser
# Website:  http://127.0.0.1:8000
# Admin:    http://127.0.0.1:8000/admin
```

---

## 📁 Project Structure

```
jn_building_products/
├── jn_building_products/     # Main config
│   ├── settings.py
│   └── urls.py
│
├── core/           # Homepage, About, Site Settings
├── products/       # Product catalog + categories
├── services/       # Construction services
├── projects/       # Completed projects + gallery
├── gallery/        # Image gallery
├── contacts/       # Contact form + inquiry management
│
├── templates/      # All HTML templates
├── static/         # CSS, JS, Images
│   └── images/
│       ├── logo.png        ← PUT YOUR LOGO HERE
│       ├── hero-bg.jpg     ← Hero background image
│       └── hero-building.jpg ← Hero side image
│
└── media/          # Uploaded images (auto-created)
```

---

## 🖼️ Adding Your Logo & Images

Place these files in `static/images/`:

| File | Description |
|------|-------------|
| `logo.png` | Your J&N logo (transparent background recommended) |
| `hero-bg.jpg` | Dark background for hero section |
| `hero-building.jpg` | Building/construction photo for hero |

Then run: `python manage.py collectstatic`

---

## ⚙️ Admin Panel Guide

Go to **http://127.0.0.1:8000/admin** and do this in order:

### Step 1: Site Settings
- Company name, phone, WhatsApp number, address
- Hero section heading and text
- Statistics (years experience, projects done, clients)

### Step 2: Product Categories
- Create categories first (e.g., "Cement", "Roofing", "Tiles")

### Step 3: Products
- Add products with images
- Mark featured ones to show on homepage

### Step 4: Services
- Add construction services
- Mark featured ones for homepage

### Step 5: Projects
- Add completed projects with cover image
- Use inline to add multiple project images
- Mark featured for homepage display

### Step 6: Testimonials
- Add client reviews (1–5 stars)

---

## 📱 WhatsApp Integration

WhatsApp is integrated in multiple places:
- Floating button (bottom-right of every page)
- Product enquiry buttons
- Contact page button
- Footer
- CTA section

To update the WhatsApp number:
→ Admin → Site Settings → WhatsApp Number
Format: `+265XXXXXXXXX` (include country code)

---

## 🌐 Deployment (PythonAnywhere - Free)

1. Create account at pythonanywhere.com
2. Upload project files
3. Create a web app (Django)
4. Set `WSGI_APPLICATION` path
5. Run `python manage.py collectstatic`
6. Set `DEBUG = False` in settings.py
7. Add your domain to `ALLOWED_HOSTS`

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2
- **Database**: SQLite (upgrade to PostgreSQL for production)
- **Frontend**: Bootstrap 5 + Custom CSS
- **Fonts**: Oswald + Source Sans 3 (Google Fonts)
- **Icons**: Bootstrap Icons

---

## 📞 Pages

| URL | Page |
|-----|------|
| `/` | Homepage |
| `/about/` | About Us |
| `/products/` | Product Catalog |
| `/products/<slug>/` | Product Detail |
| `/services/` | Services |
| `/services/<slug>/` | Service Detail |
| `/projects/` | Projects |
| `/projects/<slug>/` | Project Detail |
| `/gallery/` | Image Gallery |
| `/contact/` | Contact Form |
| `/admin/` | Admin Panel |
