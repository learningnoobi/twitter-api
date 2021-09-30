from django.urls import path
from .import views


urlpatterns = [
   path('notification_list/', views.NotificationView)
]
    