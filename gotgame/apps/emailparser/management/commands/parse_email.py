import sys
import email
import re

from django.core.management.base import BaseCommand

from emailparser.helpers import FakeEmailParser


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        import sys

        import pusher

        pusher.app_id = '42602'
        pusher.key = '03a4b4dc53485d77490b'
        pusher.secret = '4f0d6a61c3c105ae96d0'

        p = pusher.Pusher()

        p['game'].trigger('end', 
            {
                'winner': '1',
                '1': {
                    'winner': True,
                    'credits': 2,
                    'score': 3
                },
                '2': {
                    'winner': False,
                    'credits': 0,
                    'score': 0
                }
            })
        
        
        # # msg = email.message_from_string(sys.stdin.read())
        # 
        # parser = FakeEmailParser(sys.stdin.read())
        # parser.parse_message()
        # 