from django.conf import settings

def template_settings(request):
    return {
    	'site_name': settings.SITE_NAME, 
    	'site_desc': settings.SITE_DESC, 
    	'site_url': settings.SITE_URL,
    	'BASE_URL': 'http://' + request.get_host(),
    	}