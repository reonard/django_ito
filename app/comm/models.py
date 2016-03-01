# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


priorityType = (('0', '一般'), ('1', '加急'), ('2', '紧急'), ('3', '灾难'))

statusType = (('0', 'Created'),
              ('1', 'Waiting'),
              ('2', 'Resolved'),
              ('3', 'Pending'),
              ('4', 'Handling'),
              ('5', 'Closed'))


class BaseDepartment(models.Model):
    department_name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.department_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username_cn = models.CharField(max_length=32)
    department = models.ForeignKey(BaseDepartment)
    title = models.CharField(max_length=32)


class BasePriority(models.Model):
    level = models.IntegerField()
    remark = models.CharField(choices=priorityType, max_length=20)

    def __unicode__(self):
        return self.remark


class BaseTerminalInfo(models.Model):
    terminal_no = models.CharField(max_length=15, primary_key=True)
    terminal_name = models.CharField(max_length=60)
    terminal_location = models.CharField(max_length=60)
    install_time = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.terminal_name


class BaseTicket(models.Model):
    cdate = models.DateTimeField(auto_now_add=True)
    descrip = models.TextField()
    remark = models.TextField()
    upddate = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User)
    crateDep = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=statusType)
    priority = models.ForeignKey(BasePriority)
    department = models.ForeignKey(BaseDepartment)

    class Meta:
        abstract = True
