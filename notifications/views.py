from rest_framework import viewsets, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def NotificationView(request):
    noti_count = Notification.objects.filter(
        to_user=request.user,
        user_has_seen=False
    )
    serializer = NotificationSerializer(noti_count, many=True, context={
                                        'noti_count': noti_count.count(),
                                        'request':request
                                        })
    return Response(serializer.data)
