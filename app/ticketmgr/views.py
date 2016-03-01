# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required

from app.comm.role_required import role_required


# Create your views here.

from app.ticketmgr.forms import IncidentForm, ActionForm, User, BaseDepartment
from app.ticketmgr.models import Incident


@login_required
def index(request):
    incident_list = Incident.objects.all()
    paginator = Paginator(incident_list, 10)

    page = request.GET.get('page')
    try:
        incidents = paginator.page(page)
    except PageNotAnInteger:
        incidents = paginator.page(1)
    return render(request, 'ticketmgr/index.html', {'incidents': incidents})


@permission_required('ticketmgr.add_incident', "/error_no_perm/")
def create_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            print request.__dict__.items()
            new_incident = form.save(commit=False)
            new_incident.creator = User.objects.get(username=request.user)
            new_incident.status = '0'
            new_incident.save()
            form.save_m2m()
            return HttpResponseRedirect("/ticketmgr/index/")
        else:
            print form.errors
    else:
        form = IncidentForm()

    return render(request, 'ticketmgr/create_incident.html', {'form': form})


@permission_required('ticketmgr.change_incident', "/error_no_perm/")
@role_required("creator", "/error_no_perm/")
def update_incident(request, incident_id):
    if request.method == 'POST':
        form = IncidentForm(request.POST, instance=Incident.objects.get(pk=incident_id))
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/ticketmgr/index/")
        else:
            print form.errors
    else:
        print incident_id
        form = IncidentForm(instance=Incident.objects.get(pk=incident_id))

        print Incident.objects.get(pk=incident_id)
    return render(request, 'ticketmgr/update_incident.html', {'form': form})


@login_required
def show_ticket(request, incident_id):
    incident = get_object_or_404(Incident, pk=incident_id)
    form = ActionForm()
    action = incident.incidentaction_set.all().order_by('action_time')
    for act in action:
        print act.action_time
    return render(request, 'ticketmgr/incident.html', {'incident': incident, 'form': form, 'action': action})


@permission_required('ticketmgr.add_incidentaction', "/error_no_perm/")
@role_required("owner", "/error_no_perm/")
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

            incident.status = new_action.action_type
            incident.save()

            return HttpResponseRedirect("/ticketmgr/detail/"+incident_id+"/")

        else:
            incident = get_object_or_404(Incident, pk=incident_id)
            action = incident.incidentaction_set.all().order_by('action_time')
    else:
        form = ActionForm()

    return render(request, 'ticketmgr/incident.html', {'incident': incident, 'form': form, 'action': action})
    # return render(request, 'ticketmgr/create_action.html', {'form': form, 'incident_id': incident_id})
