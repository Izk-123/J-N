from django.db import models


class ConstructionConfig(models.Model):
    """
    All site configuration for the Construction sub-site.
    Admin can change every word, colour, and image without touching code.
    """
    # Brand
    company_name   = models.CharField(max_length=200, default="J&N Construction")
    tagline        = models.CharField(max_length=300, default="Building Tomorrow, Today")
    logo           = models.ImageField(upload_to='construction/brand/', blank=True, null=True)
    favicon        = models.ImageField(upload_to='construction/brand/', blank=True, null=True)

    # Colours (CSS hex — used in templates via context)
    primary_color  = models.CharField(max_length=7, default="#1A56DB", help_text="Hex e.g. #1A56DB")
    accent_color   = models.CharField(max_length=7, default="#0C2D6B", help_text="Hex e.g. #0C2D6B")

    # Contact
    phone          = models.CharField(max_length=20, blank=True)
    email          = models.EmailField(blank=True)
    address        = models.TextField(blank=True)
    whatsapp       = models.CharField(max_length=20, blank=True)

    # Social
    facebook       = models.URLField(blank=True)
    instagram      = models.URLField(blank=True)
    linkedin       = models.URLField(blank=True)

    # Hero
    hero_heading   = models.CharField(max_length=300, default="Building Excellence")
    hero_sub       = models.TextField(default="Professional construction services across Malawi.")
    hero_image     = models.ImageField(upload_to='construction/hero/', blank=True, null=True)
    hero_video_url = models.URLField(blank=True, help_text="Optional YouTube/Vimeo background video URL")

    # About
    about_text     = models.TextField(blank=True)
    about_image    = models.ImageField(upload_to='construction/about/', blank=True, null=True)
    years_exp      = models.PositiveIntegerField(default=1)
    projects_done  = models.PositiveIntegerField(default=0)
    clients        = models.PositiveIntegerField(default=0)
    
    page_header_image = models.ImageField(
        upload_to='construction/page_headers/',
        blank=True,
        null=True,
        help_text="Background image for all inner pages (About, Services, Projects, Contact)."
    )

    # SEO
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Construction Site Config"
        verbose_name_plural = "Construction Site Config"

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


class ConstructionService(models.Model):
    title             = models.CharField(max_length=200)
    slug              = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300)
    description       = models.TextField()
    icon              = models.CharField(max_length=60, default='bi-building', help_text="Bootstrap icon class")
    image             = models.ImageField(upload_to='construction/services/', blank=True, null=True)
    is_featured       = models.BooleanField(default=False)
    order             = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class ConstructionProject(models.Model):
    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True)
    description     = models.TextField()
    location        = models.CharField(max_length=200, blank=True)
    client          = models.CharField(max_length=100, blank=True)
    value           = models.CharField(max_length=100, blank=True, help_text="e.g. MK 50 million")
    completion_date = models.DateField(null=True, blank=True)
    cover_image     = models.ImageField(upload_to='construction/projects/', blank=True, null=True)
    is_featured     = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completion_date', '-created_at']

    def __str__(self):
        return self.title


class ConstructionProjectImage(models.Model):
    project = models.ForeignKey(ConstructionProject, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='construction/project_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order   = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class TeamMember(models.Model):
    name       = models.CharField(max_length=100)
    role       = models.CharField(max_length=100)
    bio        = models.TextField(blank=True)
    photo      = models.ImageField(upload_to='construction/team/', blank=True, null=True)
    order      = models.PositiveIntegerField(default=0)
    is_active  = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.role}"

class ConstructionFact(models.Model):
    title = models.CharField(max_length=100, help_text="e.g. Construction, Mechanical, Architecture")
    description = models.TextField(help_text="Short paragraph shown on the fact card")
    image = models.ImageField(upload_to='construction/facts/', help_text="Background image for this card")
    number = models.PositiveIntegerField(default=1, help_text="Display number like 01, 02, 03...")
    link_url = models.CharField(max_length=200, blank=True, help_text="e.g. /construction/services/")
    link_text = models.CharField(max_length=50, default="READ MORE")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'number']
        verbose_name = "Construction Fact"
        verbose_name_plural = "Construction Facts"

    def __str__(self):
        return f"{self.number} – {self.title}"