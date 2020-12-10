from time import sleep
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from .models import Endpoint, EndpointStatus
from .cron_task_dbupdate import update_endpoint_status

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def scheduled_tasks():
    every_fifteen_seconds()
    every_thirty_seconds()


def get_req(url):
    try:
        begin_time = datetime.now()
        if url[3] == 'GET':
            response = requests.get(url[2], verify=False, timeout=(2, 3))
        if url[3] == 'HEAD':
            response = requests.head(url[2], verify=False, timeout=(2, 3))
        if url[3] == 'OPTIONS':
            response = requests.options(url[2], verify=False, timeout=(2, 3))
        status_code = str(response.status_code)
        response_time = datetime.now() - begin_time
        if re.search(r"^2[0-9][0-9]$", status_code):
            state = 'up'
            status = 'success'

        if re.search(r"^4[0-9][0-9]$", status_code):
            state = 'down'
            status = 'Client error'

        if re.search(r"^5[0-9][0-9]$", status_code):
            state = 'down'
            status = 'Server error'

    except requests.ConnectionError as e:
        state = 'down'
        status = "Connection error"
        status_code = '0'
        response_time = timedelta(seconds=0)

    return [url[0], state, status, status_code, repr(int(response_time.total_seconds()*1000)),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")]


def runner(url_query_set):
    threads =[]
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in url_query_set:
            threads.append(executor.submit(get_req, url))

        for task in as_completed(threads):
            # print(task.result())
            update_endpoint_status(task)
            # with open('output.txt', 'a') as f:
            #     f.write(repr(task.result()))
            #     f.write("\n")


def every_fifteen_seconds():
    endpoints_list = Endpoint.objects.filter(interval='15').values_list('id', 'name', 'url', 'method')
    count = 0
    if len(endpoints_list) > 0:
        while count <= 60:
            runner(endpoints_list)
            sleep(12)
            count = count + 15


def every_thirty_seconds():
    endpoints_list = Endpoint.objects.filter(interval='30').values_list('id', 'name', 'url', 'method')
    count = 0
    if len(endpoints_list) > 0:
        while count <= 60:
            runner(endpoints_list)
            sleep(27)
            count = count + 30
