import logging

from django.core.management.base import BaseCommand

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

            log_processor = LogProcessor()
            log_processor.populate_logs(link=link)
