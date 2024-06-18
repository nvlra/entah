import asyncio
import websockets
import json
from random import randint
from colorama import Fore, Style, Back
from time import sleep
import sys

class Battle:
    def __init__(self):
        self.url = 'https://api-clicker.pixelverse.xyz/api/users'

        with open('./config.json', 'r') as file:
            config = json.load(file)
            
        self.secret = config['secret']
        self.tgId = config['tgId']
        self.initData = config['initData']
        self.hitRate = config['hitRate']
        self.websocket: websockets.WebSocketClientProtocol = None
        self.battleId = ""
        self.superHit: bool = False
        self.strike = {
            "defense": False,
            "attack": False
        }
        self.stop_event = asyncio.Event()
    
    async def sendHit(self):
        while not self.stop_event.is_set():
            if self.superHit:
                await asyncio.sleep(0.3)
                continue
            
            content = [
                "HIT",
                {
                    "battleId": self.battleId
                }
            ]
            try:
                await self.websocket.send(f"42{json.dumps(content)}")
            except:
                return
            await asyncio.sleep(self.hitRate)


    async def listenerMsg(self):
        while not self.stop_event.is_set():
            try:
                data = await self.websocket.recv()
            except:
                return
            
            if data.startswith('42'):
                data = json.loads(data.removeprefix('42'))
                if data[0] == "HIT":
                    print(f"\r🎈 {Fore.MAGENTA+Style.BRIGHT}[ Battle ]\t\t: {self.player1['name']} ({data[1]['player1']['energy']}) 👀 ({data[1]['player2']['energy']}) {self.player2['name']}", end="\r", flush=True)
                elif data[0] == "SET_SUPER_HIT_PREPARE":
                    self.superHit = True
                    pass
                elif data[0] == "SET_SUPER_HIT_ATTACK_ZONE":
                    content = [
                        "SET_SUPER_HIT_ATTACK_ZONE",
                        {
                            "battleId": self.battleId,
                            "zone": randint(1, 4)
                        }
                    ]
                    await self.websocket.send(f"42{json.dumps(content)}")
                    self.strike['attack'] = True
                elif data[0] == "SET_SUPER_HIT_DEFEND_ZONE":
                    content = [
                        "SET_SUPER_HIT_DEFEND_ZONE",
                        {
                            "battleId": self.battleId,
                            "zone": randint(1, 4)
                        }
                    ]
                    await self.websocket.send(f"42{json.dumps(content)}")
                    self.strike['defense'] = True
                elif data[0] == "END":
                    result = data[1]['result']
                    reward = data[1]['reward']
                    sleep(0.3)
                    print('')
                    if result=='WIN':
                        print(f"🍏 {Fore.MAGENTA+Style.BRIGHT}[ Battle ]\t\t: {result} {reward} Koin")
                    else:
                        print(f"🍎 {Fore.MAGENTA+Style.BRIGHT}[ Battle ]\t\t: {result} {reward} Koin")
                    
                    await self.websocket.recv()   
                    self.stop_event.set()
                    
                    return
                
                try:
                    if ( self.strike['attack'] and not self.strike['defense'] ) or ( self.strike['defense'] and not self.strike['attack'] ):
                        await self.websocket.recv()
                        await self.websocket.recv()
                
                    if self.strike['attack'] and self.strike['defense']:
                        deux = await self.websocket.recv()
                        
                        await self.websocket.send("3")
                        await self.websocket.recv()

                        self.superHit = False          
                except:
                    pass


    async def connect(self):
        uri = "wss://api-clicker.pixelverse.xyz/socket.io/?EIO=4&transport=websocket"
        async with websockets.connect(uri) as websocket:
            self.websocket = websocket
            data = await websocket.recv()
            content = {
                "tg-id": self.tgId,
                "secret": self.secret,
                "initData": self.initData
            }

            await websocket.send(f"40{json.dumps(content)}" )
            await websocket.recv()
            
            data = await websocket.recv()
            data = json.loads(data.removeprefix('42'))
            self.battleId = data[1]['battleId']
            self.player1 = {
                "name": data[1]['player1']['username']
            }
            self.player2 = {
                "name": data[1]['player2']['username']
            }

            for i in range(5, 0, -1):
                print(f"\r👻 {Fore.MAGENTA+Style.BRIGHT}[ Battle ]\t\t: Pertarungan Dimulai Dalam {i} Detik", end="\r", flush=True)
                await asyncio.sleep(1)
            
            print('')

            listenerMsgTask = asyncio.create_task(self.listenerMsg())
            hitTask = asyncio.create_task(self.sendHit())

            await listenerMsgTask
            await hitTask

            print('')