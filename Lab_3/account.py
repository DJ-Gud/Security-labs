import requests
from  dateutil import parser as dataparser
from requests.exceptions import RequestException
from enum import Enum
from cracks import *


class CasinoMode(Enum):
    Lcg = 'Lcg'
    Mt = 'Mt'
    BetterMt = 'BetterMt'


class CasionClient():
    cracks = {
        CasinoMode.Lcg: LCGCrack,
        CasinoMode.Mt: MtCracker,
        CasinoMode.BetterMt: BetterMtCracker,
    }
    
    def __init__(self, id, mode, createacc=True):
        self.id = id
        self.real_numbers = []
        self.balance = 0
        self.mode = mode
        self.del_date = None
        
        if createacc:
            self.createacc()
        
    def createacc(self):
        url = 'http://95.217.177.249/casino/createacc'
        
        resp = requests.get(url, {'id': self.id})
        resp_json = resp.json()
        
        if resp.ok:
            self.balance = resp_json.get('money')
            self.del_date = dataparser.parse(resp_json['deletionTime'])
        else:
            raise RequestException(resp_json.get('error'))
            
    def play(self, bet, number):
        url = f'http://95.217.177.249/casino/play{self.mode.value}'
        bet_params = {'id': self.id, 'bet': bet, 'number': number}
        
        resp = requests.get(url, params=bet_params)
        resp_json = resp.json()
        
        if resp.ok:
            self.balance = resp_json.get('account').get('money')
            self.real_numbers.append(resp_json.get('realNumber'))
            self._play_resp = resp_json
        else:
            raise RequestException(resp_json.get('error'))
            
    def become_a_billionaire(self):
        crack = self.cracks[self.mode](self)
        while self.balance < 1e9:
            winning_num = crack.predict()
            self.play(self.balance, winning_num)
            
        print('You just became a billionaire!')
