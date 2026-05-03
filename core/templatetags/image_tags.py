from django import template

register = template.Library()


@register.filter
def image_url(image_field, default=''):
    """
    Safely return image URL or a placeholder.
    Usage: {{ product.image|image_url }}
           {{ product.image|image_url:'https://placehold.co/600x400' }}
    """
    try:
        if image_field and image_field.name:
            return image_field.url
    except (ValueError, AttributeError):
        pass
    return default or 'https://placehold.co/600x400/1A1A1A/FFFFFF?text=No+Image'


@register.simple_tag
def safe_image_url(image_field, width=600, height=400, text='No+Image'):
    """
    Returns image URL or a sized placeholder.
    Usage: {% safe_image_url product.image 600 400 'Product' %}
    """
    try:
        if image_field and image_field.name:
            return image_field.url
    except (ValueError, AttributeError):
        pass
    return f'https://placehold.co/{width}x{height}/1A1A1A/FFFFFF?text={text}'
