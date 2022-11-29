from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/', include('users.urls')),
    path('api/', include('chats.urls')),
    path('api/', include('msges.urls')),
]
