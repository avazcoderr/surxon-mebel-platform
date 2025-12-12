from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os

@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for Railway deployment"""
    static_files_exist = os.path.exists(settings.STATIC_ROOT)
    media_files_exist = os.path.exists(settings.MEDIA_ROOT)
    
    return JsonResponse({
        'status': 'healthy',
        'static_root': settings.STATIC_ROOT,
        'static_url': settings.STATIC_URL,
        'media_root': settings.MEDIA_ROOT,
        'media_url': settings.MEDIA_URL,
        'static_files_exist': static_files_exist,
        'media_files_exist': media_files_exist,
        'debug': settings.DEBUG,
    })