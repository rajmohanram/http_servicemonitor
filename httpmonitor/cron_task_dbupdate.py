from .models import Endpoint, EndpointStatus

# [10, 'up', 'success', '200', '113', '2020-11-19 14:19:00']
# [6, 'down', 'Connection error', None, '0', '2020-11-19 14:19:00']


def update_endpoint_status(task_output):
    result = task_output.result()
    endpoint = EndpointStatus.objects.filter(name_id=result[0])
    endpoint_obj = Endpoint.objects.get(id=result[0])

    if not endpoint:
        endpoint_record = EndpointStatus(name = endpoint_obj,
                                         state = result[1],
                                         status = result[2],
                                         status_code = result[3],
                                         response_time = result[4],
                                         last_updated = result[5],
                                         down_from = result[5])
        endpoint_record.save()

    else:
        if endpoint[0].state == result[1]:
            """state not changes"""
            EndpointStatus.objects.filter(name = endpoint_obj).update(status = result[2], status_code = result[3],
                                                                      response_time = result[4],
                                                                      last_updated = result[5])
        else:
            """state changed"""
            EndpointStatus.objects.filter(name=endpoint_obj).update(state = result[1], status=result[2],
                                                                    status_code=result[3],
                                                                    response_time=result[4],
                                                                    last_updated=result[5],
                                                                    down_from = result[5])