from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_email_notification, send_sms_notification

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        notification = serializer.save()
        
        if notification.notification_type == 'email':
            send_email_notification.delay(notification.id)
        elif notification.notification_type == 'sms':
            send_sms_notification.delay(notification.id)

            