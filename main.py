from Battle import Battle
from Pixelverse import UserPixel
from random import randint
import asyncio
from colorama import Fore, Style, init 
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
        
        print(f"🤖 {Fore.CYAN+Style.BRIGHT}[ {userInfo['username']} ]")
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
                sleep(randint(5, 10)*5)
            else:
                print(err)
                sleep(randint(5, 10))