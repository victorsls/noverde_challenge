from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
                  path('obtain-auth-token/', obtain_auth_token),
                  path('', include('challenge.loan.urls', namespace='loan')),
              ] + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
