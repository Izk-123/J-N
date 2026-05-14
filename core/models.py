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
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, help_text="e.g. Homeowner, Contractor")
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★"


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
    Controls the cinematic hero, company cards, and group story.
    """
    group_name     = models.CharField(max_length=200, default="J&N Group of Companies")
    tagline        = models.CharField(max_length=300, default="Industrial Excellence For The Future")
    sub_tagline    = models.CharField(max_length=300, default="Construction · Mining · Manufacturing")
    logo           = models.ImageField(upload_to='group/brand/', blank=True, null=True)
    hero_image     = models.ImageField(upload_to='group/hero/', blank=True, null=True,
                                       help_text="Full-screen background image for the hero")
    hero_video_url = models.URLField(blank=True, help_text="Optional YouTube embed ID for background video")

    # Four company buttons (Building Products, Construction, Mining, Timber)
    btn1_label     = models.CharField(max_length=100, default="Blue Rock Wall Putty")
    btn1_url       = models.CharField(max_length=200, default="/products/")
    btn1_icon      = models.CharField(max_length=60, default="bi-droplet-fill")

    btn2_label     = models.CharField(max_length=100, default="Construction Company")
    btn2_url       = models.CharField(max_length=200, default="/construction/")
    btn2_icon      = models.CharField(max_length=60, default="bi-building")

    btn3_label     = models.CharField(max_length=100, default="Mining Company")
    btn3_url       = models.CharField(max_length=200, default="/mining/")
    btn3_icon      = models.CharField(max_length=60, default="bi-gem")

    btn4_label     = models.CharField(max_length=100, default="Timber Company")
    btn4_url       = models.CharField(max_length=200, default="/timber/")
    btn4_icon      = models.CharField(max_length=60, default="bi-tree-fill")

    # Group story section
    story_heading  = models.CharField(max_length=200, default="About the Group")
    story_text     = models.TextField(default="J&N Group of Companies is a diversified industrial group based in Malawi, delivering excellence across building products, construction, and mining.")

    # Contact
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

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'phone': '+265 000 000 000',
            'address': 'Blantyre, Malawi',
            'whatsapp': '+265000000000',
        })
        return obj
