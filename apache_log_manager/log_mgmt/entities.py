from collections import namedtuple


LogItem = namedtuple(
    "LogItem",
    ["ip_address", "log_date", "HTTP_method", "URI", "response_code", "response_size", "referer", "user_agent"],
)
