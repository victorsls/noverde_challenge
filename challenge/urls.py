from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
                  path('', admin.site.urls),
                  path('obtain-auth-token/', obtain_auth_token),
              ] + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
