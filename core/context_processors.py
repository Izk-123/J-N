from django.urls import resolve, Resolver404
from core.models import SiteSettings, GroupConfig


def site_settings(request):
    """
    Injects the correct site config into every template based on the active URL namespace.
    group/root → GroupConfig + SiteSettings
    products   → BuildingSettings
    construction → ConstructionConfig
    mining     → MiningConfig
    timber     → TimberSettings
    """
    ctx = {
        'site': SiteSettings.get_settings(),
        'gcfg': GroupConfig.get(),
    }

    try:
        match = resolve(request.path_info)
        ns = match.app_name or match.namespace or ''

        if ns == 'products' or request.path_info.startswith('/products/'):
            from products.models import BuildingSettings
            bsite = BuildingSettings.get()
            ctx['site'] = bsite
            ctx['bsite'] = bsite

        elif ns == 'construction' or request.path_info.startswith('/construction/'):
            from construction.models import ConstructionConfig
            csite = ConstructionConfig.get()
            ctx['site'] = csite
            ctx['csite'] = csite

        elif ns == 'mining' or request.path_info.startswith('/mining/'):
            from mining.models import MiningConfig
            msite = MiningConfig.get()
            ctx['site'] = msite
            ctx['msite'] = msite

        elif ns == 'timber' or request.path_info.startswith('/timber/'):
            from timber.models import TimberSettings
            tsite = TimberSettings.get()
            ctx['site'] = tsite
            ctx['tsite'] = tsite

    except (Resolver404, Exception):
        pass

    return ctx
