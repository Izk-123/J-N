from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class e.g. bi-bricks")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    specifications = models.TextField(blank=True, help_text="Technical specs, sizes, materials etc.")
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Optional")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, help_text="Average rating 0–5")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name


class BuildingSettings(models.Model):
    """Singleton config for the Blue Rock Wall Putty / Building Products sub-site."""
    company_name     = models.CharField(max_length=200, default="Blue Rock Wall Putty")
    tagline          = models.CharField(max_length=300, default="Smoothest Finish, Strongest Walls")
    logo             = models.ImageField(upload_to='products/logo/', blank=True, null=True)
    hero_heading     = models.CharField(max_length=300, default="Premium Wall Putty in Malawi")
    hero_subheading  = models.TextField(default="Quality wall putty for every surface.")
    hero_badge_text  = models.CharField(max_length=200, default="Trusted Since 2010")
    hero_image       = models.ImageField(upload_to='products/hero/', blank=True, null=True)
    phone            = models.CharField(max_length=20, blank=True)
    email            = models.EmailField(blank=True)
    address          = models.TextField(blank=True)
    whatsapp         = models.CharField(max_length=20, blank=True)
    about_text       = models.TextField(blank=True)
    primary_color    = models.CharField(max_length=7, default="#1e3a8a")
    secondary_color  = models.CharField(max_length=7, default="#FFFFFF")
    facebook         = models.URLField(blank=True)
    instagram        = models.URLField(blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Building Products Config"
        verbose_name_plural = "Building Products Config"

    def __str__(self):
        return self.company_name

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
