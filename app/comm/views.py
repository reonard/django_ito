# -*- coding: utf-8 -*-

from json import dumps

from django.shortcuts import render
from django.http import HttpResponse

from app.comm.models import BaseTerminalInfo, BaseDepartment


def error_no_perm(request):
    return render(request, "error_no_perm.html")


def get_terminal_info(request):
    if request.method == 'GET':
        resdata = {}
        try:
            terminal_no = request.GET.get('terminal_no', None)
            terminal_obj = BaseTerminalInfo.objects.get(terminal_no=terminal_no)
            resdata['terminal_name'] = terminal_obj.terminal_name
            resdata['terminal_location'] = terminal_obj.terminal_location
            return HttpResponse(dumps(resdata), content_type='application/json')
        except:
            resdata['terminal_name'] = ""
            resdata['terminal_location'] = ""
            return HttpResponse(dumps(resdata), content_type='application/json')


def get_owner(request):
    if request.method == 'GET':
        resdata = {}
        try:
            department = request.GET.get('department', None)
            owner_hint = request.GET.get('owner_hint', None)
            dep_user_set = BaseDepartment.objects.get(department_name=department).userprofile_set
            target_user = dep_user_set.filter(username_cn__contains=owner_hint).values("username_cn")
            user_list = map(lambda x: x['username_cn'], target_user)
            print user_list
            resdata['user_list'] = user_list
        except:
            resdata['user_list'] = ""
        finally:
            return HttpResponse(dumps(resdata), content_type='application/json')
            # return HttpResponse(user_list, content_type='application/json')
