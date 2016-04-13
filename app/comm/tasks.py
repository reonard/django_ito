__author__ = 'reonard'

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def async_sendmail(subject, msg_content, receiver):
    print subject
    send_mail(subject, msg_content, "reonard@163.com", receiver)