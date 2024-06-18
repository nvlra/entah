from Battle import Battle
from Pixelverse import UserPixel
from random import randint
import asyncio
from colorama import Fore, Style, init, Back 
import os
from time import sleep

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
clear()

def split_chunk(var):
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

async def main():
    init()

    user = UserPixel()

    while True:
        userInfo = user.getUser()
        stats = user.getStats()
        claim = user.claim()
        
        print(f"🤖 {Fore.CYAN+Style.BRIGHT}[ {userInfo['username']} ]")
        print(f"🪙 {Fore.YELLOW+Style.BRIGHT}[ Claim ]\t\t: {int(claim['claimedAmount'])} Koin Diklaim")
        print(f"💰 {Fore.YELLOW+Style.BRIGHT}[ Balance ]\t\t: {split_chunk(str(int(userInfo['clicksCount'])))} Koin")
        print(f"🍏 {Fore.GREEN+Style.BRIGHT}[ Wins ]\t\t: {split_chunk(str(stats['wins']))} Kali")
        print(f"🍓 {Fore.RED+Style.BRIGHT}[ Loses ]\t\t: {split_chunk(str(stats['loses']))} Kali")
        print(f"🫐 {Fore.BLUE+Style.BRIGHT}[ Total Games ]\t: {split_chunk(str(stats['battlesCount']))} Kali")
        print(f"📈 {Fore.GREEN+Style.BRIGHT}[ Money Won ]\t: {split_chunk(str(stats['winsReward']))} Koin")
        print(f"📉 {Fore.RED+Style.BRIGHT}[ Money Lost ]\t: {split_chunk(str(stats['losesReward']))} Koin")
        print(f"🚀 {Fore.BLUE+Style.BRIGHT}[ Total Earned ]\t: {split_chunk(str(stats['winsReward'] - stats['losesReward']))} Koin")
        print('')
        
        battle = Battle()
        await battle.connect()
        del battle

        user.upgradePets()
        
        for i in range(randint(5, 10), 0, -1):
            print(f"\r🤖 {Fore.CYAN+Style.BRIGHT}[ Bot ]\t\t: Mohon Tunggu {i} Detik", end="", flush=True)
            await asyncio.sleep(1)
        
        clear()   

if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())       
        except KeyboardInterrupt:
            print(f"👋🏻 [ Dadah ]")
            break
        except Exception as err:
            clear()
            print(f"💥 [ Bot Crashed ]")
            pixelverse = UserPixel()
            if pixelverse.isBroken():
                print(f"Pixelverse seems to be down for the moment, retrying again in 5 minutes ...")
                sleep(60*5)
            else:
                print("The problem does not come from the server, try to restart the bot or if the problem persist open a ticket with a screen of this error ...")
                print(err)
                print("Trying again in 60 seconds ...")

                sleep(60)
                