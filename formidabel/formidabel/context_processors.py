from django.conf import settings


def google_analytics(request):
    return {'google_analytics_code': settings.GOOGLE_ANALYTICS_CODE}
