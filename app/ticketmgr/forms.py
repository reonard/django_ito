# -*- coding: utf-8 -*-
from django import forms

from app.ticketmgr.models import Incident, IncidentAction, actionType
from app.comm.models import BasePriority, BaseTerminalInfo, BaseDepartment, User, UserProfile
from datetime import datetime


class IncidentForm(forms.ModelForm):
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.all(), to_field_name='remark')
    terminal_no = forms.ModelChoiceField(queryset=BaseTerminalInfo.objects.all(), widget=forms.TextInput,
                                         to_field_name='terminal_no')
    department = forms.ModelChoiceField(queryset=BaseDepartment.objects.all(), to_field_name='department_name')
    owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                   widget=forms.TextInput(attrs={"data-provide": "typeahead"}), to_field_name='userprofile__username_cn')
    deliver_time = forms.DateTimeField(initial=datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"))
    take_time = forms.DateTimeField(initial=datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"))

    class Meta:
        model = Incident
        fields = ['descrip', 'remark', 'priority', 'terminal_no', 'department', 'owner',
                  'package_id', 'postman_mobile', 'take_mobile', 'box_no', 'case_from', 'deliver_time', 'take_time']
        widgets = {'descrip': forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
                   'remark':  forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
                   }


class ActionForm(forms.ModelForm):
    action_type = forms.CharField(widget=forms.Select(choices=actionType))
    assign_to_dep = forms.ModelChoiceField(queryset=BaseDepartment.objects.all(), required=False, to_field_name='department_name')

    assign_to_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False,
                                            widget=forms.TextInput(attrs={"data-provide": "typeahead"}),
                                            to_field_name='userprofile__username_cn')

    class Meta:
        model = IncidentAction
        fields = ['action_type', 'action_brief', 'action_detail', 'assign_to_dep', 'assign_to_user']
        widgets = {'action_detail': forms.Textarea(attrs={"class": "form-control"})}

