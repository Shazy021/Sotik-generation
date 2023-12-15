from aiogram import Bot, Dispatcher
import bot_service
from database import postgesql

service = bot_service.BotService()
spark = postgesql.PostgreDB()

bot: Bot = Bot(token=service.BOT_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher()
