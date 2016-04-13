# -*- coding: utf-8 -*-
from django import forms

from app.issuemgr.models import Problem, ProblemAction
from app.comm.models import actionType
from app.comm.models import BasePriority, BaseTerminalInfo, BaseDepartment, User, UserProfile


class ProblemForm(forms.ModelForm):
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.all(), to_field_name='remark')
    department = forms.ModelChoiceField(queryset=BaseDepartment.objects.all(), to_field_name='department_name')
    owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                   widget=forms.TextInput(attrs={"data-provide": "typeahead"}), to_field_name='userprofile__username_cn')

    class Meta:
        model = Problem
        fields = ['descrip', 'remark', 'priority', 'department', 'owner']
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
        model = ProblemAction
        fields = ['action_type', 'action_brief', 'action_detail', 'assign_to_dep', 'assign_to_user']
        widgets = {'action_detail': forms.Textarea(attrs={"class": "form-control"})}

