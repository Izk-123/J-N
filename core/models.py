from django.db import models


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
