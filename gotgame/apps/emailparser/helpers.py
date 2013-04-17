"""
Email Parsers need to set:

* Gamers tags (both players)
* Unique Game ID
* Wining player ID

"""

import email
import re

class BaseEmailParser(object):
    def __init__(self, message_string):
        self.msg = email.message_from_string(message_string)
        self.msg_body = self.msg.get_payload()


class FakeEmailParser(BaseEmailParser):
    
    def is_draw(self, results):
        if sum(results['scores'])/2 == results['scores'][0]:
            return True
        return False
    
    def parse_message(self):
        body = self.msg_body
        # print repr(body)
        results = {
            'players': [],
            'scores': []
        }
        for player, score in re.findall(r"^([a-zA-Z0-9]+): ([0-9]+)$", self.msg_body, re.MULTILINE):
            results['players'].append(player)
            results['scores'].append(int(score))
        
        results['unique_code'] = re.search("The unique code for this game is: ([0-9]+)", body).groups(1)[0]
        results['draw'] = self.is_draw(results)
        
        
        return results