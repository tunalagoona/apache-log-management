from django.db import models


class Parser(models.Model):
    ip_address = models.CharField('IP address', max_length=200)
    log_date = models.DateTimeField('log date')
    http_method = models.CharField(max_length=200)
    uri = models.CharField(max_length=200)
    response_code = models.IntegerField('response code')
    response_size = models.CharField(max_length=200)
    referer = models.CharField('Referer', max_length=200)
    user_agent = models.CharField('User Agent', max_length=200)
