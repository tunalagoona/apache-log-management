from django.db import models


class ApacheLogs(models.Model):
    ip_address = models.CharField("IP address", max_length=200)
    log_date = models.DateTimeField("Log date", default=None, db_index=True)
    HTTP_method = models.CharField(max_length=200, db_index=True)
    URI = models.CharField(max_length=700)
    response_code = models.IntegerField("Response code", db_index=True)
    response_size = models.CharField(max_length=200)
    referer = models.CharField("Referer", max_length=400, default=None)
    user_agent = models.CharField("User Agent", max_length=400, default=None)
