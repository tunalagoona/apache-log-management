import datetime

from django.test import TestCase
from .log_processor import LogProcessor


class ParserTestCase(TestCase):
    def test_parser_parses_correctly(self):
        """Log lines are correctly parsed"""
        line = '13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] ' \
               '"GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 ' \
               'HTTP/1.1" 200 32653 "-" "Mozilla/5.0 (compatible; bingbot/2.0; ' \
               '+http://www.bing.com/bingbot.htm)" "-"'

        if line != "\n" and line != "":
            log_item = LogProcessor().parse_log_line(line)

            self.assertEqual(log_item.ip_address, "13.66.139.0")
            self.assertEqual(log_item.log_date, datetime.datetime(
                year=2020,
                month=12,
                day=19,
                hour=13,
                minute=57,
                second=26,
                tzinfo=datetime.timezone(datetime.timedelta(hours=1))
            ))
            self.assertEqual(log_item.HTTP_method, "GET")
            self.assertEqual(
                log_item.URI,
                "/index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53"
            )
            self.assertEqual(log_item.response_code, 200)
            self.assertEqual(log_item.response_size, 32653)
            self.assertEqual(log_item.referer, "-")
            self.assertEqual(
                log_item.user_agent,
                "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
            )
