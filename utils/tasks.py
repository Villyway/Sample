from __future__ import absolute_import, unicode_literals

import datetime
from celery import Celery
from celery.decorators import periodic_task
from celery.schedules import crontab
from celery import shared_task, Task

from django.utils import timezone
from django.conf import settings

from .views import GenerateNotitication, encode_data, count_days_by_dates
from .constants import NotificationTypes, NotificationStatuses, EntityTypes, Action
from .models import Notification
from users.models import UserNotification, User
from products.models import CreditBucket

app = Celery()
generate = GenerateNotitication()


@shared_task
def generate_notification(message, user_list, notification_type, create, status):
    message = generate.generate_message(
        message[0], message[1], message[2],
        message[3], message[4], message[5],
        message[6])
    users = []
    [users.append(User.objects.single_user(id)) for id in user_list]
    notification = generate.create_notification(
        users, notification_type, message, create, status)


@shared_task
def expire_notification():
    creditbuckets = CreditBucket.objects.filter(
        is_active=True).order_by('expiry_date')
    today = datetime.datetime.today()

    for creditbucket in creditbuckets:
        if count_days_by_dates(today, creditbucket.expiry_date.replace(tzinfo=None)) == 30 or count_days_by_dates(today, creditbucket.expiry_date.replace(tzinfo=None)) == 23 or count_days_by_dates(today, creditbucket.expiry_date.replace(tzinfo=None)) == 16 or count_days_by_dates(today, creditbucket.expiry_date.replace(tzinfo=None)) == 9 or count_days_by_dates(today, creditbucket.expiry_date.replace(tzinfo=None)) == 2 or count_days_by_dates(today, creditbucket.expiry_date.replace(tzinfo=None)) == 1:
            uid = encode_data(str(creditbucket.account.id))
            message = generate.generate_message(EntityTypes.ACCOUNT.value, uid, creditbucket.user.name,
                                                EntityTypes.CREDIT_BUCKET.value, str(creditbucket.id), creditbucket.user.name, Action.CREDIT_EXPIRE.value)
            generate.generate_notification(
                creditbucket.user, NotificationTypes.CREDIT.value, message, creditbucket.user.id)
        elif (creditbucket.expiry_date.replace(tzinfo=None)-today).days == 0:
            creditbucket.is_active = False
            creditbucket.save()
