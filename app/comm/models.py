# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


priorityType = (('1', '普通'), ('2', '加急'), ('3', '紧急'), ('4', '灾难'))
actionType = (('1', '解决'), ('2', '接手'), ('3', '搁置'), ('4', '转出'), ('5', '重开'))
statusType = (('0', '新建'),
              ('1', '已解决'),
              ('2', '处理中'),
              ('3', '搁置中'),
              ('4', '等待接手'),
              ('5', '已重开'))


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
    maintainer = models.ForeignKey(User)

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

    def notify_user(self,action_type):
        raise NotImplementedError

    class Meta:
        abstract = True


class BaseAction(models.Model):
    action_type = models.CharField(max_length=30, choices=actionType)
    action_brief = models.CharField(max_length=64, verbose_name="Action Brief")
    action_detail = models.TextField(max_length=256, blank=True, verbose_name="Action Detail")
    action_time = models.DateTimeField(auto_now=True)

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    class Meta:
        abstract = True