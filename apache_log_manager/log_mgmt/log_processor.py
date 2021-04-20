import logging
import os
import requests
from os import path
from typing import List
from datetime import datetime

from apachelogs import LogParser

from .entities import LogItem
from .models import Parser

logging.basicConfig(
    filename="log/log.log", format="%(levelname)s %(asctime)s: %(message)s", level=logging.DEBUG, filemode="w+"
)


class LP:
    def parse(
        self, link: str = None
    ) -> List[LogItem]:  # change logic of working with links and when write to file is needed, divide into methods
        file_path = "../extra/log_history.txt"
        if link is not None:
            r = requests.get(link)
            if r.status_code == 200:
                if not path.isfile(file_path) or os.stat(file_path).st_size == 0:
                    logging.debug("Write log history to the file")
                    with open(file_path, "w+") as f:
                        f.write(r.text)
        else:
            parser = LogParser('%h %l %u %{[%d/%b/%Y:%H:%M:%S %z]}t "%r" %>s %b "%{Referer}i" "%{User-agent}i"')

            with open(file_path, "r") as f:
                logs = []
                for l in f.readlines():
                    if l != "\n":
                        line = l[:-5]  # Remove '-' symbol from the end of the line as the field is of no value(explain)

                        entry = parser.parse(line)

                        http_method = entry.request_line.split()[0]  # check if these fields are set correctly
                        uri = entry.request_line.split()[1] if entry.request_line.split()[1] is not None else "-"  # wtf
                        response_code = entry.final_status if entry.final_status is not None else "-"
                        response_size = entry.bytes_sent if entry.bytes_sent is not None else "-"

                        date_and_time = entry.request_time_fields

                        log_date = datetime(
                            year=int(date_and_time["year"]),
                            month=int(datetime.strptime(date_and_time["abbrev_mon"], "%b").month),
                            day=int(date_and_time["mday"]),
                            hour=int(date_and_time["hour"]),
                            minute=int(date_and_time["min"]),
                            second=int(date_and_time["sec"]),
                            tzinfo=date_and_time["timezone"]
                        )

                        referer = entry.headers_in["Referer"] if entry.headers_in["Referer"] is not None else "-"
                        user_agent = entry.headers_in["User-Agent"] if entry.headers_in["User-Agent"] is not None else "-"

                        log_line = LogItem(
                            ip_address=entry.remote_host,
                            log_date=log_date,
                            http_method=http_method,
                            uri=uri,
                            response_code=response_code,
                            response_size=response_size,
                            referer=referer,
                            user_agent=user_agent,
                        )
                        logging.debug(f"log line: {log_line}")

                        logs.append(log_line)
        return logs

    def write_to_db(self, logs: List[LogItem]):
        for log in logs:
            p = Parser(**log._asdict())
            p.save()


if __name__ == "__main__":
    lp = LP()
    # web_link = "http://www.almhuette-raith.at/apache-log/access.log"
    lp.parse()
