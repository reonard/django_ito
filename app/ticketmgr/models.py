# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from app.comm.models import BaseTicket, BaseTerminalInfo, BaseDepartment



# Create your models here.

ticketType = (('I', 'Incident'), ('P', 'Problem'), ('S', 'ServiceRequest'))
actionType = (('1', 'Re-Assign'), ('2', 'Resolve'), ('3', 'Suspend'), ('4', 'Takeover'), ('5', 'Close'))
statusType = (('0', 'Created'),
              ('1', 'Waiting'), ('2', 'Resolved'), ('3', 'Pending'), ('4', 'Handling'), ('5', 'Closed'))

sourceType = (('0', 'ServicePhone'), ('1', 'WeChat'), ('2', 'Operator'), ('3', 'Other'))


class Incident(BaseTicket):
    terminal_no = models.ForeignKey(BaseTerminalInfo)
    owner = models.ForeignKey(User, related_name="incident_owner")
    package_id = models.CharField(max_length=50, blank=True)
    postman_mobile = models.CharField(max_length=20, blank=True)
    take_mobile = models.CharField(max_length=20, blank=True)
    box_no = models.CharField(max_length=5, blank=True)
    case_from = models.CharField(max_length=20, choices=sourceType, blank=True)
    deliver_time = models.DateTimeField(null=True)  # Todo change to datetime field
    take_time = models.DateTimeField(null=True)  # Todo change to datetime field

    def update(self, **kwargs):
        print kwargs
        print self.__dict__
        self.__dict__.update(kwargs)
        print self.__dict__

    def __unicode__(self):
        return self.descrip


class Problem(BaseTicket):
    pass


class ServReq(BaseTicket):
    pass


class BaseAction(models.Model):
    action_type = models.CharField(max_length=30, choices=actionType)
    action_brief = models.CharField(max_length=64, blank=True, verbose_name="Action Brief")
    action_detail = models.TextField(max_length=256, blank=True, verbose_name="Action Detail")
    action_time = models.DateTimeField(auto_now=True)

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    class Meta:
        abstract = True


class IncidentAction(BaseAction):
    action_for = models.ForeignKey(Incident)
    assign_to_dep = models.ForeignKey(BaseDepartment, blank=True, null=True)
    assign_to_user = models.ForeignKey(User, blank=True, null=True)
    creator = models.ForeignKey(User, related_name="incident_action_creator")



