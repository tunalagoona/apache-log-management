import logging
import os
import requests
from collections import namedtuple
from os import path
from typing import List, Dict

from apachelogs import LogParser


logging.basicConfig(
    filename="../log/log.log", format="%(levelname)s %(asctime)s: %(message)s", level=logging.DEBUG, filemode="w+"
)


LogItem = namedtuple(
    "LogItem",
    ["ip_address", "log_date", "http_method", "uri", "response_code", "response_size", "referer", "user_agent"],
)


class LP:
    def parse(
        self, link: str = None
    ) -> List[LogItem]:  # change logic of working with links and when write to file is needed
        if link is not None:
            r = requests.get(link)
            if r.status_code == 200:
                if (
                    not path.isfile("../../extra/log_history.txt")
                    or os.stat("../../extra/log_history.txt").st_size == 0
                ):
                    logging.debug("Write log history to the file")
                    with open("../../extra/log_history.txt", "w+") as f:
                        f.write(r.text)
        else:
            parser = LogParser('%h %l %u %{[%d/%b/%Y:%H:%M:%S %z]}t "%r" %>s %b "%{Referer}i" "%{User-agent}i"')

            with open("../../extra/log_history.txt", "r") as f:
                logs = []
                for l in f.readlines():
                    if l != "\n":
                        line = l[:-5]  # Remove '-' symbol from the end of the line as the field is of no value(explain)

                        entry = parser.parse(line)

                        http_method = entry.request_line.split()[0]  # check if these fields are set correctly
                        uri = entry.request_line.split()[1]

                        log_line = LogItem(
                            ip_address=entry.remote_host,
                            log_date=entry.request_time_fields,
                            http_method=http_method,
                            uri=uri,
                            response_code=entry.final_status,
                            response_size=entry.bytes_sent,
                            referer=entry.headers_in["Referer"],
                            user_agent=entry.headers_in["User-Agent"],
                        )
                        logging.debug(f"log line: {log_line}")

                        logs.append(log_line)
        return logs


if __name__ == "__main__":
    lp = LP()
    # web_link = "http://www.almhuette-raith.at/apache-log/access.log"
    lp.parse()
