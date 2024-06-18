import requests
import json

class UserPixel:
    def __init__(self):
        with open('./config.json', 'r') as file:
            self.config = json.load(file)
            
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "secret": self.config['secret'],
            "tg-id": self.config['tgId'],
            "initData": self.config['initData']
        }
    
    def getUser(self):
        url = "https://api-clicker.pixelverse.xyz/api/users"
        req = requests.get(url, headers=self.headers)
        return req.json()
    
    def getStats(self):
        url = "https://api-clicker.pixelverse.xyz/api/battles/my/stats"
        req = requests.get(url, headers=self.headers)
        return req.json()
    
    def isBroken(self):
        url = "https://api-clicker.pixelverse.xyz/api/tasks/my"
        req = requests.get(url, headers=self.headers)
        return req.status_code == 500