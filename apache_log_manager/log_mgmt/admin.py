from django.contrib import admin

from .models import Parser


class ParserAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "log_date",
        "HTTP_method",
        "URI",
        "response_code",
        "response_size",
        "referer",
        "user_agent",
    )
    list_filter = ("response_code", "HTTP_method", "log_date")
    search_fields = (
        "ip_address",
        "log_date",
        "HTTP_method",
        "URI",
        "response_code",
        "response_size",
        "referer",
        "user_agent",
    )


admin.site.register(Parser, ParserAdmin)
