import logging
import os
import requests
from collections import namedtuple
from os import path
from typing import List, Dict

from apachelogs import LogParser


logging.basicConfig(filename="../log/log.log", format='%(levelname)s %(asctime)s: %(message)s', level=logging.DEBUG, filemode="w+")


LogItem = namedtuple("LogItem", ["ip_address", "log_date", "http_method", "uri", "response_code", "response_size"])


class LP:
    def parse(self, link: str = None):
        if link is not None:
            r = requests.get(link)
            if r.status_code == 200:
                if not path.isfile("../../extra/log_history.txt") \
                        or os.stat("../../extra/log_history.txt").st_size == 0:
                    logging.debug("Write log history to the file")
                    with open("../../extra/log_history.txt", "w+") as f:
                        f.write(r.text)
        else:
            parser = LogParser("%h %l %u %{[%d/%b/%Y:%H:%M:%S %z]}t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"")

            # parser = LogParser("%>s")

            with open("../../extra/log_history.txt", "r") as f:
                line = '13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] "GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 HTTP/1.1" 200 32653 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"'
                # line = '200'
                logging.debug(f"line: {line}")
                entry = parser.parse(line)
                logging.debug(f"remote_host: {entry.remote_host}")
                logging.debug(f"request_time: {entry.request_time_fields}")
                logging.debug(f"request_line: {entry.request_line}")
                logging.debug(f"final_status: {entry.final_status}")
                logging.debug(f"bytes_sent: {entry.bytes_sent}")
                logging.debug(f"headers_in['Referer']: {entry.headers_in['Referer']}")
                logging.debug(f"headers_in['User-Agent']: {entry.headers_in['User-Agent']}")


        #             LogItem(ip_address=ip_address)
        #
        # return LogItem()


lp = LP()
# web_link = "http://www.almhuette-raith.at/apache-log/access.log"
lp.parse()
