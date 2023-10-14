import os
import requests
from colorama import init, Fore
from dotenv import load_dotenv


class BotService:
    def __init__(self):
        load_dotenv()
        init(autoreset=True)
        try:
            self.BOT_TOKEN = os.getenv("BOT_TOKEN")
            if self.validate_token(self.BOT_TOKEN):
                print(Fore.GREEN + f"{self.bot_username} has successfully connected to telegram")
            else:
                print(Fore.RED + 'Invalid bot token')
        except:
            print(Fore.RED + 'please add your telegram bot token in the env file')
            exit

    def validate_token(self, bot_token):
        url = f'https://api.telegram.org/bot{bot_token}/getMe'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data["ok"]:
            self.bot_username = data["result"]['username']
            return True
        else:
            return False