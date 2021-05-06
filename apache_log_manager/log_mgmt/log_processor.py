import logging
from datetime import datetime
from typing import Optional

import requests
from tqdm import tqdm
from apachelogs import LogParser

from .entities import LogItem
from .models import ApacheLogs

logger = logging.getLogger()


class LogProcessor:
    def __init__(self):
        # Pattern for parsing Apache log entries
        self.parser = LogParser('%h %l %u %{[%d/%b/%Y:%H:%M:%S %z]}t "%r" %>s %b "%{Referer}i" "%{User-agent}i"')

    def populate_logs(self, link: str = None):
        """Download Apache logs using the supplied link, then parse them and load into the database."""
        if link:
            response = requests.get(link)
            logger.info(f"Status code is {response.status_code}")
            if response.status_code != 200:
                return None

            lines = response.text.splitlines()

            with tqdm(total=len(lines), leave=False) as progress_bar:
                progress_bar.set_description(f"Processing Apache log entries")

                batch_size = 64
                objs = []

                # Parse log lines and insert batches to the database.
                for line in lines:
                    if line != "\n" and line != "":
                        log_item = self.parse_log_line(line)
                        objs.append(ApacheLogs(**log_item._asdict()))

                        if len(objs) == batch_size:
                            ApacheLogs.objects.bulk_create(objs, batch_size)
                            progress_bar.update(n=batch_size)
                            objs.clear()

                ApacheLogs.objects.bulk_create(objs, len(objs))
                progress_bar.update(n=len(objs))

    def parse_log_line(self, line: str) -> LogItem:
        """Parse the log line."""
        # Removing '-' from the end of the line before parsing
        line = line[:-4]

        entry = self.parser.parse(line)
        parsed_log_line = LogProcessor.convert_to_logitem(entry)
        logger.debug(f"parsed log line: {parsed_log_line}")

        return parsed_log_line

    @staticmethod
    def convert_to_logitem(entry) -> LogItem:
        """Convert LogParser entry into LogItem."""

        def sub(x: Optional):
            return "-" if x is None else x

        http_method = sub(entry.request_line.split()[0])
        uri = sub(entry.request_line.split()[1])
        response_code = sub(entry.final_status)
        response_size = sub(entry.bytes_sent)
        referer = sub(entry.headers_in["Referer"])
        user_agent = sub(entry.headers_in["User-Agent"])

        dt = entry.request_time_fields
        log_date = datetime(
            year=int(dt["year"]),
            month=int(datetime.strptime(dt["abbrev_mon"], "%b").month),
            day=int(dt["mday"]),
            hour=int(dt["hour"]),
            minute=int(dt["min"]),
            second=int(dt["sec"]),
            tzinfo=dt["timezone"],
        )

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
