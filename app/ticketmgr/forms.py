# -*- coding: utf-8 -*-
from django import forms

from app.ticketmgr.models import Incident, IncidentAction
from app.issuemgr.models import Problem
from app.comm.models import actionType
from app.comm.models import BasePriority, BaseTerminalInfo, BaseDepartment, User, UserProfile
from datetime import datetime
from django.utils.translation import ugettext as _


class IncidentForm(forms.ModelForm):
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.all(),
                                      to_field_name='level',
                                      initial=1,
                                      label=_("priority"))
    relate_to_prob = forms.ModelChoiceField(queryset=Problem.objects.all(),
                                            to_field_name='id',
                                            label=_("relate_to_prob"))
    terminal_no = forms.ModelChoiceField(queryset=BaseTerminalInfo.objects.all(),
                                         widget=forms.TextInput,
                                         to_field_name='terminal_no',
                                         label=_("terminal_no"))
    department = forms.ModelChoiceField(queryset=BaseDepartment.objects.all(),
                                        to_field_name='id',
                                        label=_("department"))
    owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                   widget=forms.TextInput(attrs={"data-provide": "typeahead"}),
                                   to_field_name='userprofile__username_cn',
                                   label=_("owner"))
    deliver_time = forms.DateTimeField(initial=datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
                                       label=_("deliver_time"))
    take_time = forms.DateTimeField(initial=datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
                                    label=_("take_time"))

    class Meta:
        model = Incident
        fields = ['descrip', 'remark', 'priority', 'terminal_no', 'department', 'owner', 'relate_to_prob',
                  'package_id', 'postman_mobile', 'take_mobile', 'box_no', 'case_from', 'deliver_time', 'take_time']

        widgets = {'descrip': forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
                   'remark':  forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
                   }

        labels = {}
        for field in fields:
            labels[field] = _(field)

class ActionForm(forms.ModelForm):
    action_type = forms.CharField(widget=forms.Select(choices=actionType),
                                  label=_("action_type"))
    assign_to_dep = forms.ModelChoiceField(queryset=BaseDepartment.objects.all(),
                                           required=False,
                                           to_field_name='id',
                                           label=_("assign_to_dep"))

    assign_to_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False,
                                            widget=forms.TextInput(attrs={"data-provide": "typeahead"}),
                                            to_field_name='userprofile__username_cn',
                                            label=_("assign_to_user"))

    class Meta:
        model = IncidentAction
        fields = ['action_type', 'assign_to_dep', 'assign_to_user', 'action_brief', 'action_detail']
        widgets = {'action_detail': forms.Textarea(attrs={"class": "form-control"})}
        labels = {}
        for field in fields:
            labels[field] = _(field)


