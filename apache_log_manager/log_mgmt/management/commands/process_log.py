from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import logging
from typing import List

from apachelogs import LogParser

from ...entities import LogItem
from ...log_processor import LP


logging.basicConfig(
    filename="../../log/log.log", format="%(levelname)s %(asctime)s: %(message)s", level=logging.DEBUG, filemode="w+"
)


class Command(BaseCommand):
    help = 'Processes the specified link containing Apache logs'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        lp = LP()
        logs: List[LogItem] = lp.parse()
        self.stdout.write("Parse finished")
        self.stdout.write(f"logs found: {logs[0]}")
        self.stdout.write("Start writing to DB")
        lp.write_to_db(logs)
        self.stdout.write(f"write completed")
