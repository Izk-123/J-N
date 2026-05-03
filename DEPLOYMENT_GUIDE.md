# 🚀 Deploying J&N Building Products to PythonAnywhere

This guide will get your website live on the internet — **free** — in under 30 minutes.

---

## What You'll Get

- **Live URL**: `yourusername.pythonanywhere.com`
- Free hosting (upgrade later for a custom domain like `jnbuildingproducts.mw`)
- Runs 24/7 on the internet
- Full Django admin at `/admin/`

---

## Step 1 — Create a PythonAnywhere Account

1. Go to **https://www.pythonanywhere.com**
2. Click **"Start running Python online in less than a minute!"**
3. Choose **"Create a Beginner account"** (free)
4. Pick a username — this becomes part of your URL, e.g. `jnbuilding.pythonanywhere.com`
5. Verify your email

---

## Step 2 — Upload Your Project Files

### Option A: Upload the ZIP (easiest)

1. In PythonAnywhere, go to **Files** tab
2. Click **Upload a file**
3. Upload `jn_building_products_phase2.zip`
4. Open a **Bash console** (from the Dashboard)
5. Run:
```bash
cd ~
unzip jn_building_products_phase2.zip
ls   # you should see the jn_building_products/ folder
```

### Option B: Use Git (if you have a GitHub repo)

```bash
cd ~
git clone https://github.com/yourusername/jn_building_products.git
```

---

## Step 3 — Create a Virtual Environment

In the PythonAnywhere **Bash console**:

```bash
# Create virtual environment (use Python 3.10 or 3.11)
mkvirtualenv jnenv --python=/usr/bin/python3.10

# Make sure it's activated (you should see "(jnenv)" in your prompt)
workon jnenv

# Install dependencies
cd ~/jn_building_products
pip install -r requirements.txt
```

---

## Step 4 — Edit Production Settings

```bash
nano jn_building_products/settings_production.py
```

Find these lines and update them:

```python
ALLOWED_HOSTS = [
    'jnbuilding.pythonanywhere.com',   # ← YOUR username here
]

EMAIL_HOST_USER = 'yourgmail@gmail.com'         # ← Your Gmail
EMAIL_HOST_PASSWORD = 'your-app-password'       # ← Gmail App Password
DEFAULT_FROM_EMAIL = 'J&N Building Products <yourgmail@gmail.com>'
ADMIN_EMAIL = 'yourgmail@gmail.com'             # ← Where form emails go
```

Save: press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 5 — Set Up the Database & Static Files

Still in Bash console:

```bash
cd ~/jn_building_products
workon jnenv

# Run migrations
python manage.py migrate --settings=jn_building_products.settings_production

# Load sample data (optional — skip if you have real data)
python manage.py load_sample_data --settings=jn_building_products.settings_production

# Create your admin login
python manage.py createsuperuser --settings=jn_building_products.settings_production

# Collect all static files (CSS, JS, images)
python manage.py collectstatic --settings=jn_building_products.settings_production
```

---

## Step 6 — Configure the Web App

1. Go to **Web** tab in PythonAnywhere
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"** (not Django wizard)
4. Select **Python 3.10**

### Set the Source Code path:
```
/home/yourusername/jn_building_products
```

### Set the Working Directory:
```
/home/yourusername/jn_building_products
```

### Set the Virtualenv path:
```
/home/yourusername/.virtualenvs/jnenv
```

---

## Step 7 — Configure the WSGI File

1. In the Web tab, click the WSGI configuration file link (looks like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
2. **Delete everything** in that file
3. **Paste** the contents of `pythonanywhere_wsgi.py` from your project
4. Change `yourusername` to your actual PythonAnywhere username (appears 2 times)
5. Click **Save**

---

## Step 8 — Set Up Static Files

Still in the Web tab, scroll to **Static files** section:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/jn_building_products/staticfiles` |
| `/media/` | `/home/yourusername/jn_building_products/media` |

Click **Save** after adding both.

---

## Step 9 — Reload & Test!

1. Click the big green **"Reload"** button in the Web tab
2. Visit `https://yourusername.pythonanywhere.com`
3. Your site should be live! 🎉
4. Visit `https://yourusername.pythonanywhere.com/admin/` to log in

---

## 🔧 Troubleshooting

### White screen / 500 error
Check the error log: Web tab → **Error log**

### Static files not loading (no CSS)
```bash
workon jnenv
cd ~/jn_building_products
python manage.py collectstatic --settings=jn_building_products.settings_production
```
Then reload the web app.

### "DisallowedHost" error
Add your domain to `ALLOWED_HOSTS` in `settings_production.py`

### Images not showing
Make sure the `/media/` static files mapping is set correctly in the Web tab.

---

## Step 10 — Add Your Real Logo

1. In PythonAnywhere Files tab, navigate to:
   `jn_building_products/static/images/`
2. Upload your `logo.png` file
3. Run `collectstatic` again
4. Reload the web app

---

## 📧 Setting Up Gmail for Contact Form Emails

You need a **Gmail App Password** (not your regular password):

1. Go to your Google Account: **https://myaccount.google.com**
2. Click **Security** → **2-Step Verification** (enable if not already on)
3. Go back to Security → scroll down to **App passwords**
4. Create one: App = "Mail", Device = "Other (Custom name)" → type "JN Website"
5. Google gives you a 16-character password — paste it into `settings_production.py`

---

## 🌐 Custom Domain (Optional — paid feature)

If you want `jnbuildingproducts.mw` or `.com`:

1. Upgrade to PythonAnywhere **Hacker plan** ($5/month)
2. Go to Web tab → Add a custom domain
3. Update your domain's DNS records to point to PythonAnywhere
4. Add the domain to `ALLOWED_HOSTS`

---

## 📅 Keeping It Updated

When you make changes to the code:

```bash
# In PythonAnywhere Bash console:
workon jnenv
cd ~/jn_building_products

# Pull latest changes (if using Git)
git pull

# Apply any new migrations
python manage.py migrate --settings=jn_building_products.settings_production

# Collect static files if CSS/JS changed
python manage.py collectstatic --settings=jn_building_products.settings_production

# Then in the Web tab: click Reload
```

---

## ✅ Deployment Checklist

- [ ] PythonAnywhere account created
- [ ] Project files uploaded
- [ ] Virtual environment created (`jnenv`)
- [ ] `requirements.txt` installed
- [ ] `settings_production.py` updated with your details
- [ ] Database migrated
- [ ] Superuser created
- [ ] Static files collected
- [ ] Web app configured
- [ ] WSGI file updated
- [ ] Static file mappings set (`/static/` and `/media/`)
- [ ] Web app reloaded
- [ ] Site is live and accessible
- [ ] Admin panel works
- [ ] Contact form sends emails
- [ ] Logo uploaded

---

*Built by J&N Building Products development team — "Make Your House Smile"*
