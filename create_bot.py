from aiogram import Bot, Dispatcher
import bot_service

service = bot_service.BotService()

bot: Bot = Bot(token=service.BOT_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher()