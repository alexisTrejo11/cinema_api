from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from twilio.rest import Client
from .models import Notification
import logging

logger = logging.getLogger(__name__)

def send_email_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        
        send_mail(
            subject="Cinema Booking Update",
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient],
            fail_silently=False,
        )
        
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")

def send_sms_notification(notification_id):
    if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER]):
        logger.error("Twilio credentials not configured")
        return

    try:
        notification = Notification.objects.get(id=notification_id)
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=notification.message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=notification.recipient
        )
        
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
        
    except Exception as e:
        logger.error(f"Failed to send SMS: {str(e)}")