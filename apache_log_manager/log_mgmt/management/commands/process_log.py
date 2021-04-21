import logging
from typing import List
import requests

from django.core.management.base import BaseCommand

from ...entities import LogItem
from ...log_processor import LogProcessor

logging.basicConfig(
    filename="log/log.log", format="%(levelname)s %(asctime)s: %(message)s", level=logging.INFO, filemode="w+"
)


class Command(BaseCommand):
    help = "Processes the specified link containing Apache logs"

    def add_arguments(self, parser) -> None:
        parser.add_argument("link", nargs="+", type=str)

    def handle(self, *args, **options) -> None:
        if options["link"]:
            link = options["link"][0]
            if self.validate_url(link):
                logs: List[LogItem] = LogProcessor.parse_from_link(link=link)
                self.stdout.write("Parsing finished")
                self.stdout.write(f"logs returned[1]: {logs[1]}")
                self.stdout.write("Start writing to DB")
                LogProcessor.write_to_db(logs)
                self.stdout.write(f"Write completed")

    def validate_url(self, link) -> bool:
        try:
            response = requests.get(link)
            self.stdout.write("URL is valid and exists on the internet")
            return True
        except requests.ConnectionError as exception:
            self.stdout.write(f"URL does not exist on Internet: {exception}")
            return False
