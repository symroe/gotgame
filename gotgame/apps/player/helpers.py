import mock
import requests

TEST_DATA = """
[{"name":"dnfPercent","label":"Dnf%","type":"online","value":"2"},{"name":"wins","label":"Wins","type":"online","value":"1068"},{"name":"ties","label":"Draws","type":"online","value":"346"},{"name":"losses","label":"Losses","type":"online","value":"286"},{"name":"gamesPlayed","label":"Games Played","type":"online","value":"1700"},{"name":"streak","label":"Current Streak","type":"online","value":"-2"},{"name":"averageGoalsPerGame","label":"Goals Per Game","type":"online","value":"2.37"},{"name":"averagePossession","label":"Average Possession","type":"online","value":"51.50"},{"name":"averageShotsFor","label":"Shots For Per Game","type":"online","value":"11.00"},{"name":"averageShotsAgainst","label":"Shots Against Per Game","type":"online","value":"5.62"},{"name":"tackleSuccessRate","label":"Tackle Success %","type":"online","value":"70"},{"name":"passSuccessRate","label":"Pass Success %","type":"online","value":"79"},{"name":"averageFoulsPerGame","label":"Fouls Per Game","type":"online","value":"0.93"},{"name":"averagebookingsPerGame","label":"Bookings Per Game","type":"online","value":"0.16"},{"name":"averagecornersPerGame","label":"Corners Per Game","type":"online","value":"2.55"},{"name":"averageoffsidesPerGame","label":"Offsides Per Game","type":"online","value":"0.43"}]
"""



class EAPlayerCard(object):
    def __init__(self, player_id, platformTag='soccer-fifa-13-360'):
        self.player_id = player_id
        self.platformTag = platformTag
        self.loadCard()
    
    def loadCard(self):
        base_url = "http://www.easports.com/services/statscentral/getdata"
        args = {
            "platformTag" : "soccer-fifa-13-360",
            "mode" : "online",
            "handle" : self.player_id
        }
        res = requests.get(base_url, params=args)
        self.card_data = res.json()
        self.parse_card()
    
    def parse_card(self):
        data = self.card_data
        self.parsed_data = {}
        for item in data:
            name = item['name']
            del item['name']
            self.parsed_data[name] = item
    
    def generate_score(self):
        """
        Does some magic to make a score
        """
        # TODO Change this to something sane!
        
        data = self.parsed_data
        win_balance = int(data['wins']['value']) - int(data['losses']['value'])
        

x = EAPlayerCard("x Dodotti x")
x.generate_score()
