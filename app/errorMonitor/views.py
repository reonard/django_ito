from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from app.errorMonitor.models import ErrorDetail
from django.http import HttpResponse
from json import dumps
from django.core.paginator import Paginator
# Create your views here.


@login_required
@permission_required('errorMonitor', "/error_no_perm/")
def index(request):
    return render(request, "error_monitor/index.html")


@login_required
@permission_required('errorMonitor', "/error_no_perm/")
def ajax_error_index(request):
    data_t = {}
    if request.method == "GET":
        length = int(request.GET.get("length"))
        page = int(request.GET.get("start"))/length + 1
        print "page is %s" % page
        data_total = ErrorDetail.objects.count()
        print data_total
        data_set = ErrorDetail.objects.all().values("server_ip",
                                                    "level",
                                                    "error_msg",
                                                    "app__app_name",
                                                    "error_key__error_name",
                                                    "error_type__errorType")
        paginator = Paginator(data_set, length)

        data_t["data"] = list(paginator.page(page))
        data_t["recordsTotal"] = data_total
        data_t["recordsFiltered"] = data_total
        return HttpResponse(dumps(data_t), content_type='application/json')



