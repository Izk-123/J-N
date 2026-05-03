"""
Badge callbacks for Unfold sidebar navigation.
Referenced in settings.py UNFOLD["SIDEBAR"]["navigation"]
"""
from contacts.models import ContactMessage


def new_messages(request):
    """Returns count of unread messages as a badge string."""
    count = ContactMessage.objects.filter(status='new').count()
    return str(count) if count else None
