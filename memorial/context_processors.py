from django.conf import settings
from .models import SiteSetting


def site_settings(request):
    """Provide site-wide settings to all templates."""
    site_settings_dict = {}
    for setting in SiteSetting.objects.all():
        site_settings_dict[setting.key] = setting.value

    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Chiya Aago Memorial"),
        "SITE_TAGLINE": getattr(settings, "SITE_TAGLINE", "We Remember"),
        "SITE_DESCRIPTION": getattr(settings, "SITE_DESCRIPTION", ""),
        "custom_settings": site_settings_dict,
    }
