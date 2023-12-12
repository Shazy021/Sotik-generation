from create_bot import dp
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.client_kb import menu_markup


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message) -> None:
    await message.answer(
        f'Привет {message.from_user.first_name} 👋',
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        f'Чем могу помочь?\nВыбери команду 👇',
        reply_markup=menu_markup
    )
    await message.delete()