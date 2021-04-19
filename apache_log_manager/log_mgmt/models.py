from django.db import models


class Parser(models.Model):
    ip_address = models.CharField('IP address', max_length=200)
    log_data = models.CharField(max_length=200)
    http_method = models.CharField(max_length=200)
    uri = models.CharField(max_length=200)
    response_code = models.CharField(max_length=200)
    response_size = models.CharField(max_length=200)

    # models.DateTimeField('date published')
