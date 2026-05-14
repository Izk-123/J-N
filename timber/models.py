from django.db import models


class TimberSettings(models.Model):
    """Singleton config for the Timber sub-site — editable entirely from admin."""
    company_name    = models.CharField(max_length=200, default="J&N Timber")
    tagline         = models.CharField(max_length=300, default="Sustainable Timber, Expertly Processed")
    logo            = models.ImageField(upload_to='timber/logo/', blank=True, null=True)
    favicon         = models.ImageField(upload_to='timber/brand/', blank=True, null=True)

    primary_color   = models.CharField(max_length=7, default="#166534", help_text="Hex e.g. #166534 (Forest Green)")
    accent_color    = models.CharField(max_length=7, default="#78350F", help_text="Hex e.g. #78350F (Brown)")

    phone           = models.CharField(max_length=20, blank=True)
    email           = models.EmailField(blank=True)
    address         = models.TextField(blank=True)
    whatsapp        = models.CharField(max_length=20, blank=True)
    facebook        = models.URLField(blank=True)
    linkedin        = models.URLField(blank=True)

    hero_heading    = models.CharField(max_length=300, default="Premium Timber & Wood Processing")
    hero_sub        = models.TextField(default="From forest to finished product — quality timber for every project.")
    hero_image      = models.ImageField(upload_to='timber/hero/', blank=True, null=True)
    about_text      = models.TextField(blank=True)
    about_image     = models.ImageField(upload_to='timber/about/', blank=True, null=True)
    years_exp       = models.PositiveIntegerField(default=1)
    trees_processed = models.CharField(max_length=50, blank=True, help_text="e.g. 50,000+")
    clients         = models.PositiveIntegerField(default=0)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Timber Site Config"
        verbose_name_plural = "Timber Site Config"

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


class TimberCategory(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Timber Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class TimberProduct(models.Model):
    name           = models.CharField(max_length=200)
    slug           = models.SlugField(unique=True)
    category       = models.ForeignKey(TimberCategory, on_delete=models.CASCADE, related_name='products')
    description    = models.TextField()
    specifications = models.TextField(blank=True, help_text="Species, dimensions, grade, moisture content, treatment")
    image          = models.ImageField(upload_to='timber/products/', blank=True, null=True)
    is_featured    = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name


class TimberProject(models.Model):
    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True)
    description     = models.TextField()
    location        = models.CharField(max_length=200, blank=True)
    cover_image     = models.ImageField(upload_to='timber/projects/', blank=True, null=True)
    is_featured     = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completion_date', '-created_at']

    def __str__(self):
        return self.title
