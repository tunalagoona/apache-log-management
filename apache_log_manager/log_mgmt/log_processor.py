import logging
from datetime import datetime
from typing import List, Optional

import requests
from apachelogs import LogParser

from .entities import LogItem
from .models import Parser


logger = logging.getLogger()


class LogProcessor:
    @staticmethod
    def parse(link: str = None) -> Optional[List[LogItem]]:
        """Download and parse Apache logs from the link."""
        if link:
            r = requests.get(link)
            logger.info(f"Status code is {r.status_code}")
            if r.status_code != 200:
                return None

            parser_input = r.text

            # Pattern for parsing Apache log entries
            parser = LogParser('%h %l %u %{[%d/%b/%Y:%H:%M:%S %z]}t "%r" %>s %b "%{Referer}i" "%{User-agent}i"')

            logs = []
            for line in parser_input.splitlines():
                if line != "\n" and line != '':
                    # Remove '-' from the end of the line before parsing
                    entry = parser.parse(line[:-4])
                    parsed_log_line = LogProcessor.format_apachelogs_entry(entry)
                    logger.debug(f"parsed log line: {parsed_log_line}")
                    logs.append(parsed_log_line)

            return logs

    @staticmethod
    def format_apachelogs_entry(entry) -> LogItem:
        """Reformat LogParser entry."""
        http_method = entry.request_line.split()[0] if entry.request_line.split()[0] is not None else "-"
        uri = entry.request_line.split()[1] if entry.request_line.split()[1] is not None else "-"
        response_code = entry.final_status if entry.final_status is not None else "-"
        response_size = entry.bytes_sent if entry.bytes_sent is not None else "-"
        referer = entry.headers_in["Referer"] if entry.headers_in["Referer"] is not None else "-"
        user_agent = (entry.headers_in["User-Agent"] if entry.headers_in["User-Agent"] is not None else "-")
        date_and_time = entry.request_time_fields
        log_date = LogProcessor.make_datetime(date_and_time)

        log_line = LogItem(
            ip_address=entry.remote_host,
            log_date=log_date,
            HTTP_method=http_method,
            URI=uri,
            response_code=response_code,
            response_size=response_size,
            referer=referer,
            user_agent=user_agent,
        )
        return log_line

    @staticmethod
    def make_datetime(date_and_time) -> datetime:
        """Convert LogParser request_time_fields into datetime."""
        log_date = datetime(
            year=int(date_and_time["year"]),
            month=int(datetime.strptime(date_and_time["abbrev_mon"], "%b").month),
            day=int(date_and_time["mday"]),
            hour=int(date_and_time["hour"]),
            minute=int(date_and_time["min"]),
            second=int(date_and_time["sec"]),
            tzinfo=date_and_time["timezone"],
        )
        return log_date

    @staticmethod
    def write_to_db(logs: List[LogItem]):
        for log in logs:
            p = Parser(**log._asdict())
            p.save()
