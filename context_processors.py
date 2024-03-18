from django.utils.translation import activate, deactivate

def admin_panel_language(request):
    if request.path.startswith('/admin/') or request.path.startswith('/rosettafiles/'):
        activate('en')
    else:
        deactivate()
    return {}
