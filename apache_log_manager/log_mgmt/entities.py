from collections import namedtuple


LogItem = namedtuple(
    "LogItem",
    ["ip_address", "log_date", "http_method", "uri", "response_code", "response_size", "referer", "user_agent"],
)
