from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('tweets/', include('tweets.urls')),
    path('chat/', include('chat.urls')),
    path('notify/', include('notifications.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/',  include('djoser.urls.jwt')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
