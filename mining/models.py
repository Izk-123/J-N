from django.db import models


class MiningConfig(models.Model):
    """
    All site configuration for the Mining sub-site.
    Each field is editable from the admin — no code changes needed.
    """
    # Brand
    company_name   = models.CharField(max_length=200, default="J&N Mining")
    tagline        = models.CharField(max_length=300, default="Extracting Value From the Earth")
    logo           = models.ImageField(upload_to='mining/brand/', blank=True, null=True)
    favicon        = models.ImageField(upload_to='mining/brand/', blank=True, null=True)

    # Colours
    primary_color  = models.CharField(max_length=7, default="#B45309", help_text="Hex e.g. #B45309")
    accent_color   = models.CharField(max_length=7, default="#78350F", help_text="Hex e.g. #78350F")

    # Contact
    phone          = models.CharField(max_length=20, blank=True)
    email          = models.EmailField(blank=True)
    address        = models.TextField(blank=True)
    whatsapp       = models.CharField(max_length=20, blank=True)

    # Social
    facebook       = models.URLField(blank=True)
    linkedin       = models.URLField(blank=True)

    # Hero
    hero_heading   = models.CharField(max_length=300, default="Industrial Mining Excellence")
    hero_sub       = models.TextField(default="Responsible mineral extraction and processing in Malawi.")
    hero_image     = models.ImageField(upload_to='mining/hero/', blank=True, null=True)

    # About
    about_text     = models.TextField(blank=True)
    about_image    = models.ImageField(upload_to='mining/about/', blank=True, null=True)
    years_exp      = models.PositiveIntegerField(default=1)
    tonnes_mined   = models.CharField(max_length=50, blank=True, help_text="e.g. 50,000+")
    sites          = models.PositiveIntegerField(default=1)

    # Certifications / compliance text
    compliance_text = models.TextField(blank=True, help_text="Environmental & safety certifications")

    # SEO
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Mining Site Config"
        verbose_name_plural = "Mining Site Config"

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


class MineralCategory(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Mineral Categories"

    def __str__(self):
        return self.name


class MineralProduct(models.Model):
    name              = models.CharField(max_length=200)
    slug              = models.SlugField(unique=True)
    category          = models.ForeignKey(MineralCategory, on_delete=models.CASCADE, related_name='minerals')
    description       = models.TextField()
    specifications    = models.TextField(blank=True, help_text="Grade, purity, size, chemical composition")
    image             = models.ImageField(upload_to='mining/minerals/', blank=True, null=True)
    is_featured       = models.BooleanField(default=False)
    is_active         = models.BooleanField(default=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name


class MiningEquipment(models.Model):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    description = models.TextField()
    image       = models.ImageField(upload_to='mining/equipment/', blank=True, null=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MiningOperation(models.Model):
    """A mine site or operational area."""
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    location    = models.CharField(max_length=200)
    description = models.TextField()
    minerals    = models.ManyToManyField(MineralProduct, blank=True, related_name='operations')
    image       = models.ImageField(upload_to='mining/operations/', blank=True, null=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.name
