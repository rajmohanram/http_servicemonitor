from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Endpoint, EndpointStatus
import requests
import re

# /mweb/endpoints
@login_required()
def endpoints(request):
    """View for managing HTTP endpoint."""
    if request.method == 'GET':
        endpoints = Endpoint.objects.all()
        context = {"endpoints": endpoints}
        return render(request, 'httpmonitor/endpoints.html', context=context)
    if request.method == 'POST':
        if request.POST.get('id'):
            id = request.POST.get('id')
            name = request.POST.get('endpoint')
            url = request.POST.get('url')
            method = request.POST.get('method')
            interval = request.POST.get('interval')
            Endpoint.objects.filter(id=id).update(name=name, url=url, method=method, interval=interval)
        else:
            name = request.POST.get('endpoint')
            url = request.POST.get('url')
            interval = request.POST.get('interval')
            Endpoint.objects.create(name=name, url=url, interval=interval)
        return redirect('httpmonitor.endpoints')


# /mweb/del-endpoint?id=10
@login_required()
def del_endpoint(request):
    """View for deleting an HTTP endpoint."""
    id = request.GET.get('id')
    Endpoint.objects.filter(id=id).delete()
    return redirect('httpmonitor.endpoints')


# /mweb/get-endpoint?id=10
def get_endpoint(request):
    """View to get an HTTP endpoint detail."""
    id = request.GET.get('id')
    endpoint = Endpoint.objects.values_list('id', 'name', 'url', 'method', 'interval').get(id=id)
    return JsonResponse({"endpoint": endpoint})


# /mweb/get_services_up
def get_services_up(request):
    """View to get all HTTP endpoint detail."""
    endpoint_status = EndpointStatus.objects.filter(state='up')
    endpoint_status_list = []
    for i in endpoint_status:
        endpoint = Endpoint.objects.get(id=i.name_id)
        tmp = [endpoint.name, endpoint.url, i.status_code, i.response_time, i.last_updated]
        endpoint_status_list.append(tmp)
    return JsonResponse({"endpoints_status": endpoint_status_list})

# tmp = [endpoint.name, endpoint.url, i.status, i.down_from, i.last_updated]


# /mweb/get_services_down
def get_services_down(request):
    """View to get all HTTP endpoint detail."""
    endpoint_status = EndpointStatus.objects.filter(state='down')
    endpoint_status_list = []
    for i in endpoint_status:
        endpoint = Endpoint.objects.get(id=i.name_id)
        tmp = [endpoint.name, endpoint.url, i.status, i.down_from, i.last_updated]
        endpoint_status_list.append(tmp)
    return JsonResponse({"endpoints_status": endpoint_status_list})


# /mweb/endpoints
@login_required()
def endpoints_status(request):
    """View for checking the status of all HTTP endpoint."""
    return render(request, 'httpmonitor/endpoints-status.html')

@csrf_exempt
# /mweb/check-state
def check_state(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            response = requests.get(url, verify=False, timeout=(2, 3))
            status_code = str(response.status_code)

            if re.search(r"^4[0-9][0-9]$", status_code):
                state = 'Down'
                status = 'Client error'

            if re.search(r"^5[0-9][0-9]$", status_code):
                state = 'Down'
                status = 'Server error'

        except requests.ConnectionError as e:
            status_code = '0'
            state = 'Down'
            status = repr(e)
        state_response = [state, status_code, status]
        return JsonResponse({"response": state_response})

