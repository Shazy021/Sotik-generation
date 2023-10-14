from create_bot import dp
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message) -> None:
    await message.answer(
        f'Привет {message.from_user.first_name} 👋',
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        f'Чем могу помочь?\nВыбери команду 👇',
    )
    await message.delete()
