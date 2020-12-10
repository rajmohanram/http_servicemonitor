from django.db import models


# model: HTTP endpoint
class Endpoint(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=255, unique=True)
    method = models.CharField(max_length=30, unique=False, default='GET')
    interval = models.CharField(max_length=30, unique=False)

    def __str__(self):
        return self.name


# model: HTTP endpoint status
class EndpointStatus(models.Model):
    name = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, unique=False)
    status = models.CharField(max_length=30, null=True, unique=False)
    status_code = models.CharField(max_length=30, null=True, unique=False)
    response_time = models.CharField(max_length=30, null=True, unique=False)
    last_updated = models.CharField(max_length=30, null=True, unique=False)
    down_from = models.CharField(max_length=30, null=True, unique=False)

    # [8, 'up', 'success', '200', 23, datetime.datetime(2020, 11, 19, 13, 45, 25, 603084)]

    def __str__(self):
        return self.status

