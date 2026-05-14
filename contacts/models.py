from django.db import models


class ContactMessage(models.Model):
    SOURCE_CHOICES = (
        ('group',    'Group Landing'),
        ('products', 'Building Products'),
        ('construction', 'Construction'),
        ('mining',   'Mining'),
        ('timber',   'Timber'),
        ('general',  'General'),
    )
    STATUS_CHOICES = (
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='general',
                              help_text="Which sub-site sent this enquiry")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d %b %Y')}"
