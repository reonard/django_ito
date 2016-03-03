from __future__ import unicode_literals

from django.db import models

# Create your models here.

levelType = (('1', 'INFO'), ('2', 'WARNING'), ('3', 'Critical'))


class BaseApps(models.Model):
    app_id = models.IntegerField(primary_key=True)
    app_name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.app_name


class BaseErrorType(models.Model):
    error_id = models.IntegerField(primary_key=True)
    errorType = models.CharField(max_length=32)

    def __unicode__(self):
        return self.errorType


class BaseErrorItem(models.Model):
    error_id = models.IntegerField(primary_key=True)
    error_name = models.CharField(max_length=512)

    def __unicode__(self):
        return self.error_name


class ErrorDetail(models.Model):
    error_type = models.ForeignKey(BaseErrorType)
    level = models.CharField(max_length=32, choices=levelType)
    server_ip = models.GenericIPAddressField()
    app = models.ForeignKey(BaseApps)
    error_msg = models.CharField(max_length=2048)
    error_key = models.ForeignKey(BaseErrorItem)
    is_sendsms = models.BooleanField(default=0)
    is_sendmail = models.BooleanField(default=0)
    sms_status = models.BooleanField(default=0)
    mail_status = models.BooleanField(default=0)
    remark = models.CharField(max_length=256)
    logtime = models.DateTimeField()
