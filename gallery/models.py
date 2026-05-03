from django.db import models


class GalleryImage(models.Model):
    CATEGORY_CHOICES = (
        ('product', 'Product'),
        ('project', 'Project'),
        ('general', 'General'),
    )
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Gallery Image {self.pk}"
