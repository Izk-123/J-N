from django.db import models
from django.utils import timezone


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=200, default="J&N Building Products")
    tagline = models.CharField(max_length=300, default="Make Your House Smile")
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    whatsapp_number = models.CharField(max_length=20, help_text="Include country code e.g. +265991234567")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    hero_heading = models.CharField(max_length=300, default="Building Malawi's Future")
    hero_subheading = models.TextField(default="Quality building products and construction services you can trust.")
    about_text = models.TextField(blank=True)
    years_experience = models.PositiveIntegerField(default=1)
    projects_completed = models.PositiveIntegerField(default=0)
    happy_clients = models.PositiveIntegerField(default=0)
    # Inside SiteSettings model
    hero_badge_text = models.CharField(
        max_length=200,
        default="Trusted Building Partner in Malawi"
    )
    hero_heading_prefix = models.CharField(
        max_length=100,
        default="Building"
    )
    hero_heading_highlight = models.CharField(
        max_length=100,
        default="Malawi's"
    )
    hero_heading_suffix = models.CharField(
        max_length=100,
        default="Future"
    )
    hero_image = models.ImageField(
        upload_to='hero/',
        blank=True,
        null=True,
        help_text="Upload a hero background image. If left empty, the default static image will be used."
    )
    # About page
    about_image = models.ImageField(
        upload_to='about/', blank=True, null=True,
        help_text="Main image shown on the About page."
    )
    about_mission = models.TextField(
        blank=True,
        default="To provide affordable, high-quality building products and construction services that help Malawians build safe, beautiful, and lasting homes and structures."
    )
    about_vision = models.TextField(
        blank=True,
        default="To be the most trusted and preferred building products and construction company in Malawi — known for quality, reliability, and making every house smile."
    )
    # Value 1
    about_value1_title = models.CharField(max_length=100, default="Quality First")
    about_value1_desc = models.TextField(default="We only supply products that meet high construction standards. No shortcuts.")
    about_value1_icon = models.CharField(max_length=100, default="bi-award-fill", help_text="Bootstrap icon class")
    # Value 2
    about_value2_title = models.CharField(max_length=100, default="Customer Focused")
    about_value2_desc = models.TextField(default="Your project goals drive everything we do. We listen before we build.")
    about_value2_icon = models.CharField(max_length=100, default="bi-people-fill", help_text="Bootstrap icon class")
    # Value 3
    about_value3_title = models.CharField(max_length=100, default="Integrity Always")
    about_value3_desc = models.TextField(default="Transparent pricing and honest communication — always. No hidden costs.")
    about_value3_icon = models.CharField(max_length=100, default="bi-shield-check-fill", help_text="Bootstrap icon class")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        # Only allow one instance
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'company_name': 'J&N Building Products',
            'phone': '+265 000 000 000',
            'address': 'Blantyre, Malawi',
            'whatsapp_number': '+265000000000',
        })
        return obj

class Testimonial(models.Model):
    SOURCE_CHOICES = (
        ('group',       'Group Landing'),
        ('products',    'Building Products'),
        ('construction','Construction'),
        ('mining',      'Mining'),
        ('timber',      'Timber'),
        ('general',     'General'),
    )

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, help_text="e.g. Homeowner, Contractor")
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='general',
                              help_text="Which sub-site this testimonial is for")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★ ({self.get_source_display()})"


# ─── NEW: Visitor Analytics ─────────────────────────────────────────────

class Visitor(models.Model):
    path = models.CharField(max_length=255, help_text="Page visited")
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, default='')
    device_type = models.CharField(max_length=20, blank=True, default='')
    browser = models.CharField(max_length=100, blank=True, default='')
    referrer = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['ip_address']),
        ]
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"

    def __str__(self):
        return f"{self.ip_address} → {self.path} at {self.created_at:%H:%M}"

    @staticmethod
    def get_device_type(user_agent):
        """Simple device detection without extra packages."""
        ua = user_agent.lower()
        if 'mobile' in ua:
            return 'Mobile'
        elif 'tablet' in ua or 'ipad' in ua:
            return 'Tablet'
        return 'Desktop'

    @staticmethod
    def get_browser(user_agent):
        ua = user_agent.lower()
        if 'firefox' in ua:
            return 'Firefox'
        elif 'edge' in ua or 'edg' in ua:
            return 'Edge'
        elif 'chrome' in ua and 'safari' in ua:
            return 'Chrome'
        elif 'safari' in ua:
            return 'Safari'
        return 'Other'


class WhatsAppClick(models.Model):
    page_path = models.CharField(max_length=255)
    product = models.ForeignKey(
        'products.Product',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='whatsapp_clicks'
    )
    contact_message = models.ForeignKey(
        'contacts.ContactMessage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='whatsapp_clicks'
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "WhatsApp Click"
        verbose_name_plural = "WhatsApp Clicks"

    def __str__(self):
        return f"WhatsApp click on {self.created_at:%Y-%m-%d %H:%M}"

class GroupConfig(models.Model):
    """
    Configuration for the Group holding page (jandn.mw/).
    Now fully dynamic – every visible element is editable in admin.
    """
    # ── Brand & Hero ──────────────────────────────────────────────
    group_name     = models.CharField(max_length=200, default="J&N Pvt Limited")
    tagline        = models.CharField(max_length=300, default="Industrial Excellence For The Future")
    sub_tagline    = models.CharField(max_length=300, default="Construction · Mining · Manufacturing")
    logo           = models.ImageField(upload_to='group/brand/', blank=True, null=True)
    hero_image     = models.ImageField(upload_to='group/hero/', blank=True, null=True,
                                       help_text="Full-screen background image for the hero")
    hero_video_url = models.CharField(
        max_length=50, blank=True,
        help_text="YouTube video ID (e.g., dQw4w9WgXcQ). Leave empty to use hero_image."
    )

    # Hero text (new)
    hero_title          = models.CharField(max_length=200, default="Building Today.<br><span class='orange-text'>Empowering Tomorrow.</span>",
                                           help_text="Use <br> for line break, and <span class='orange-text'> for orange highlights.")
    hero_subheading     = models.CharField(max_length=300, default="Mining · Construction · Timber · Building Products")

    # ── Four company cards (using existing and new fields) ────────
    btn1_label     = models.CharField(max_length=100, default="Blue Rock Wall Putty")
    btn1_url       = models.CharField(max_length=200, default="/products/")
    btn1_icon      = models.CharField(max_length=60, default="bi-droplet-fill")
    card1_description = models.TextField(max_length=200, default="Blue Rock Wall Putty & premium finishes.")
    card1_bg_image = models.ImageField(
        upload_to='group/cards/', blank=True, null=True,
        help_text="Background image for Building Products card"
    )

    btn2_label     = models.CharField(max_length=100, default="Construction Company")
    btn2_url       = models.CharField(max_length=200, default="/construction/")
    btn2_icon      = models.CharField(max_length=60, default="bi-building")
    card2_description = models.TextField(max_length=200, default="Building structures, engineering the future.")
    card2_bg_image = models.ImageField(
        upload_to='group/cards/', blank=True, null=True,
        help_text="Background image for Construction card"
    )

    btn3_label     = models.CharField(max_length=100, default="Mining Company")
    btn3_url       = models.CharField(max_length=200, default="/mining/")
    btn3_icon      = models.CharField(max_length=60, default="bi-gem")
    card3_description = models.TextField(max_length=200, default="Extracting value, powering industrial progress.")
    card3_bg_image = models.ImageField(
        upload_to='group/cards/', blank=True, null=True,
        help_text="Background image for Mining card"
    )

    btn4_label     = models.CharField(max_length=100, default="Timber Company")
    btn4_url       = models.CharField(max_length=200, default="/timber/")
    btn4_icon      = models.CharField(max_length=60, default="bi-tree-fill")
    card4_description = models.TextField(max_length=200, default="Sustainable forestry & wood solutions.")
    card4_bg_image = models.ImageField(
        upload_to='group/cards/', blank=True, null=True,
        help_text="Background image for Timber card"
    )

    # ── Values strip (4 pillars) ──────────────────────────────────
    value1_title = models.CharField(max_length=100, default="Diverse Expertise")
    value1_desc  = models.CharField(max_length=200, default="Four industries, one united vision")
    value1_icon  = models.CharField(max_length=50, default="bi-gear-wide-connected")

    value2_title = models.CharField(max_length=100, default="Quality & Safety")
    value2_desc  = models.CharField(max_length=200, default="Highest international standards")
    value2_icon  = models.CharField(max_length=50, default="bi-shield-check")

    value3_title = models.CharField(max_length=100, default="Sustainability")
    value3_desc  = models.CharField(max_length=200, default="Responsible industrial growth")
    value3_icon  = models.CharField(max_length=50, default="bi-recycle")

    value4_title = models.CharField(max_length=100, default="Innovation")
    value4_desc  = models.CharField(max_length=200, default="Engineering modern Africa")
    value4_icon  = models.CharField(max_length=50, default="bi-cpu")

    # ── About section (story + stats) ─────────────────────────────
    story_heading  = models.CharField(max_length=200, default="About the Group")
    story_text     = models.TextField(default="J&N Group of Companies is a diversified industrial group based in Malawi, delivering excellence across building products, construction, and mining.")

    stat1_number = models.PositiveIntegerField(default=4, help_text="Number for first stat")
    stat1_label  = models.CharField(max_length=100, default="Strategic Sectors")
    stat2_number = models.PositiveIntegerField(default=12, help_text="Number for second stat")
    stat2_label  = models.CharField(max_length=100, default="Years Excellence")
    stat3_number = models.PositiveIntegerField(default=250, help_text="Number for third stat")
    stat3_label  = models.CharField(max_length=100, default="Industry Partners")

    # ── Parallax divider ──────────────────────────────────────────
    divider_title    = models.CharField(max_length=200, default="Unmatched Industrial Strength")
    divider_subtitle = models.CharField(max_length=200, default="Engineering Malawi's infrastructure & economy")

    # ── Footer ────────────────────────────────────────────────────
    footer_copyright = models.CharField(max_length=200, default="Industrial Excellence.")

    # ── Contact & Social (already existed, keep as is) ────────────
    phone          = models.CharField(max_length=20, blank=True)
    email          = models.EmailField(blank=True)
    address        = models.TextField(blank=True)
    whatsapp       = models.CharField(max_length=20, blank=True)
    facebook       = models.URLField(blank=True)
    linkedin       = models.URLField(blank=True)

    class Meta:
        verbose_name = "Group Site Config"
        verbose_name_plural = "Group Site Config"

    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    def get_industry_cards(self):
        """Return a list of industry card dicts for the landing page."""
        from django.templatetags.static import static
        
        cards = [
            {
                'id': 'products',
                'url': self.btn1_url,
                'icon': self.btn1_icon,
                'label': self.btn1_label,
                'description': self.card1_description,
                'button_text': 'View',
                'overlay_hue': 200,
                'bg_image': self.card1_bg_image.url if self.card1_bg_image else static('images/hero-bg.jpg'),
                'order': 4,
                'active': bool(self.btn1_url),
            },
            {
                'id': 'construction',
                'url': self.btn2_url,
                'icon': self.btn2_icon,
                'label': self.btn2_label,
                'description': self.card2_description,
                'button_text': 'Discover',
                'overlay_hue': 5,
                'bg_image': self.card2_bg_image.url if self.card2_bg_image else static('images/hero-bg.jpg'),
                'order': 2,
                'active': bool(self.btn2_url),
            },
            {
                'id': 'mining',
                'url': self.btn3_url,
                'icon': self.btn3_icon,
                'label': self.btn3_label,
                'description': self.card3_description,
                'button_text': 'Explore',
                'overlay_hue': 0,
                'bg_image': self.card3_bg_image.url if self.card3_bg_image else static('images/hero-bg.jpg'),
                'order': 1,
                'active': bool(self.btn3_url),
            },
            {
                'id': 'timber',
                'url': self.btn4_url,
                'icon': self.btn4_icon,
                'label': self.btn4_label,
                'description': self.card4_description,
                'button_text': 'Explore',
                'overlay_hue': 80,
                'bg_image': self.card4_bg_image.url if self.card4_bg_image else static('images/hero-bg.jpg'),
                'order': 3,
                'active': bool(self.btn4_url),
            },
        ]
        return sorted([c for c in cards if c['active']], key=lambda x: x['order'])

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'phone': '+265 000 000 000',
            'address': 'Blantyre, Malawi',
            'whatsapp': '+265000000000',
        })
        return obj
