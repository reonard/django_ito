# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from app.comm.models import BaseTicket, BaseTerminalInfo, BaseDepartment, BaseAction
from app.comm.global_settings import MAIL_TEMPLATE, MIALSUBJECT
from app.issuemgr.models import Problem, Cause
from app.comm.tasks import async_sendmail

# Create your models here.

ticketType = (('I', 'Incident'), ('P', 'Problem'), ('S', 'ServiceRequest'))
# statusType = (('0', '新建'),
#               ('1', '等待接手'), ('2', '已解决'), ('3', '搁置中'), ('4', '处理中'), ('5', '已重开'))
sourceType = (('0', '客服电话'), ('1', '微信'), ('2', '运维反馈'), ('3', '其他'))


def get_display(choices, key):
    def _get_display(item):
        item[key] = dict(choices)[str(item[key])]
    return _get_display


class Incident(BaseTicket):
    resolve_time = models.DateTimeField(null=True)
    relate_to_prob = models.ForeignKey(Problem, null=True, blank=True)
    major_cause = models.ForeignKey(Cause, null=True, blank=True)
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

    def re_assign(self, user):
        self.owner = user

    def update_status(self, status):
        self.status = status

    def link_to_problem(self, problem):
        self.relate_to_prob = problem

    def notify_user(self, action_type):
        msg_content = MAIL_TEMPLATE[action_type].format(incident=self)
        msg_subject = MIALSUBJECT[action_type].format(incident=self)
        receiver = self.owner.email
        async_sendmail.delay(msg_subject, msg_content, (receiver,))

    def __unicode__(self):
        return self.descrip


class IncidentAction(BaseAction):
    action_for = models.ForeignKey(Incident)
    assign_to_dep = models.ForeignKey(BaseDepartment, blank=True, null=True)
    assign_to_user = models.ForeignKey(User, blank=True, null=True)
    creator = models.ForeignKey(User, related_name="incident_action_creator")


