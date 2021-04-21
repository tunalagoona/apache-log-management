from django.db import models


class ApacheLogs(models.Model):
    ip_address = models.CharField("IP address", max_length=200)
    log_date = models.DateTimeField("Log date", default=None)
    HTTP_method = models.CharField(max_length=200)
    URI = models.CharField(max_length=200)
    response_code = models.IntegerField("Response code")
    response_size = models.CharField(max_length=200)
    referer = models.CharField("Referer", max_length=200, default=None)
    user_agent = models.CharField("User Agent", max_length=200, default=None)
