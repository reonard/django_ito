from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from app.errorMonitor.models import ErrorDetail
from django.http import HttpResponse
from json import dumps

# Create your views here.


@login_required
def index(request):
    return render(request, "error_monitor/index.html")


def ajax_error_index(request):
    data_t = {}
    if request.method == "GET":
        data_set = ErrorDetail.objects.all().values("server_ip",
                                                    "level",
                                                    "error_msg",
                                                    "app__app_name",
                                                    "error_key__error_name",
                                                    "error_type__errorType")
        data_t["data"] = list(data_set)
        return HttpResponse(dumps(data_t), content_type='application/json')



