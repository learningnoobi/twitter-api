from django.urls import path
from .import views


urlpatterns = [
    path('notification_list/', views.NotificationView),
    path('notification_seen_delete/', views.NotificationSeen.as_view()),
]
