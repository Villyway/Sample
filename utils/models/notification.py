from django.db import models

from base.models import Base
from utils.constants import NotificationTypes


class Notification(Base):
    """
    Model used for notification.
    """
    notification_type = models.CharField(
        max_length=20, choices=NotificationTypes.choices())
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.notification_type
