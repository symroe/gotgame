import sys
import email
import re

from django.core.management.base import BaseCommand

from emailparser.helpers import FakeEmailParser


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # msg = email.message_from_string(sys.stdin.read())
        
        parser = FakeEmailParser(sys.stdin.read())
        parser.parse_message()
        