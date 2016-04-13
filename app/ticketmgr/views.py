# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from json import dumps
from app.comm.role_required import role_required
from app.ticketmgr.models import get_display
from datetime import datetime
from django.forms.models import model_to_dict
from django.db import transaction

# Create your views here.

from app.ticketmgr.forms import IncidentForm, ActionForm, User, BaseDepartment
from app.ticketmgr.models import Incident
from app.issuemgr.models import Problem
from app.comm.models import statusType, priorityType, BasePriority

COL_NAME_MAP = {'0': 'id', '1': 'terminal_no__terminal_no', '2': 'terminal_no__terminal_name',
                '3': 'terminal_no__terminal_location', '4': 'priority', '5': 'owner__userprofile__username_cn',
                '6': 'department', '7': 'status', '8': 'cdate'}

@login_required
def ajax_incident_list(request):
    data_t = {}
    print request.GET
    if request.method == "GET":
        order = request.GET.get('order[0][column]')
        start = int(request.GET.get("start"))
        end = start + int(request.GET.get("length"))
        priority = request.GET.get('filter_priority')
        status = request.GET.get('filter_status')
        department = request.GET.get('filter_department')
        show_all = request.GET.get('filter_all')
        problem = request.GET.get('filter_problem')

        query_condition = {}

        if priority:
            query_condition['priority__level'] = priority
        if status:
            query_condition['status'] = status
        if department:
            query_condition['department__id'] = department
        if show_all != "true":
            query_condition['owner'] = request.user
        if problem:
            query_condition['relate_to_prob__id'] = problem


        incident_set = Incident.objects.filter(**query_condition).values("id",
                                                 "terminal_no__terminal_no",
                                                 "terminal_no__terminal_name",
                                                 "terminal_no__terminal_location",
                                                 "priority",
                                                 "owner__userprofile__username_cn",
                                                 "department__department_name",
                                                 "status",
                                                 "cdate")

        if request.GET.get('order[0][dir]') == 'asc':
            data_set = list(incident_set.order_by(COL_NAME_MAP[order]))
        else:
            data_set = list(incident_set.order_by("-" + COL_NAME_MAP[order]))

        res_data = data_set[start:end]

        for rec in res_data:
            rec['cdate'] = rec['cdate'].strftime("%Y-%m-%d")

        map(get_display(statusType, "status"), res_data)
        map(get_display(priorityType, "priority"), res_data)
        data_t["data"] = res_data
        data_t["recordsTotal"] = len(data_set)
        data_t["recordsFiltered"] = len(data_set)
        return HttpResponse(dumps(data_t), content_type='application/json')


@login_required
def index(request):
    prioritys = BasePriority.objects.all()
    deps = BaseDepartment.objects.all()
    problems = Problem.objects.all()
    return render(request, 'ticketmgr/index.html', {'prioritys': prioritys,
                                                    'statuses': statusType,
                                                    'deps': deps,
                                                    'problems': problems})


@permission_required('ticketmgr.add_incident', "/error_no_perm/")
def create_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            new_incident = form.save(commit=False)
            new_incident.creator = User.objects.get(username=request.user)
            new_incident.status = '0'
            new_incident.save()
            form.save_m2m()
            new_incident.notify_user("create")
            return HttpResponseRedirect("/ticketmgr/index/")
    else:
        form = IncidentForm()
    return render(request, 'ticketmgr/create_incident.html', {'form': form})


@permission_required('ticketmgr.change_incident', "/error_no_perm/")
@role_required("creator", 'incident', "/error_no_perm/")
def update_incident(request, incident_id):
    if request.method == 'POST':
        with transaction.atomic():
            incident = Incident.objects.select_for_update().filter(pk=incident_id)[0]
            form = IncidentForm(request.POST, instance=incident)
            if form.is_valid():
                updated_incident = form.save()
                updated_incident.notify_user("update")
                return HttpResponseRedirect("/ticketmgr/detail/%s" % incident_id)
    else:
        incident = Incident.objects.get(pk=incident_id)
        incident_data = model_to_dict(incident)
        incident_data['owner'] = incident.owner.userprofile.username_cn
        form = IncidentForm(incident_data)
    return render(request, 'ticketmgr/update_incident.html', {'form': form})


@login_required
def show_ticket(request, incident_id):
    incident = get_object_or_404(Incident, pk=incident_id)
    form = ActionForm()
    action = incident.incidentaction_set.all().order_by('action_time')
    return render(request, 'ticketmgr/incident.html', {'incident': incident, 'form': form, 'action': action})

@permission_required('ticketmgr.add_incidentaction', "/error_no_perm/")
@role_required("owner", 'incident', "/error_no_perm/")
def create_action(request, incident_id):
    if request.method == 'POST':
        form = ActionForm(request.POST)
        print request.POST
        if form.is_valid():
            new_action = form.save(commit=False)
            new_action.creator = User.objects.get(username=request.user.username)
            new_action.action_for = Incident.objects.get(pk=incident_id)
            new_action.save()
            form.save_m2m()
            # change incident owner to newly updated one
            incident = new_action.action_for

            if new_action.assign_to_user and new_action.assign_to_dep:
                incident.owner = new_action.assign_to_user
                incident.department = new_action.assign_to_dep

            #  Resolved
            if new_action.action_type == "1":
                incident.resolve_time = datetime.now()

            incident.status = new_action.action_type
            incident.save()

            # Re-Assign
            if new_action.action_type == "4":
                incident.notify_user("transfer")

            return HttpResponseRedirect("/ticketmgr/detail/"+incident_id+"/")

        else:
            incident = get_object_or_404(Incident, pk=incident_id)
            action = incident.incidentaction_set.all().order_by('action_time')
    else:
        form = ActionForm()

    return render(request, 'ticketmgr/incident.html', {'incident': incident, 'form': form, 'action': action})
