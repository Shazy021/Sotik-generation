from create_bot import dp, bot, spark
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.client_kb import menu_markup, to_menu, report_markup


@dp.message(Command(commands=['start', 'start_menu']))
async def process_start_command(message: Message) -> None:
    await message.answer(
        f'Привет {message.from_user.first_name} 👋',
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        f'Чем могу помочь?\nВыбери команду 👇',
        reply_markup=menu_markup
    )

    if message.text == '/start_menu':
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await message.delete()


@dp.callback_query(lambda callback: callback.data in ['/report'])
async def process_report_command(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.answer()

    check_db_con_message = await bot.send_message(callback.from_user.id,
                                                  f'Пожалуйста, подождите.\n'
                                                  f'Идет проверка соединения с базой данных...',
                                                  reply_markup=to_menu
                                                  )

    if spark.validate_connection('products'):
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=check_db_con_message.message_id)
        await bot.send_message(callback.from_user.id,
                               f'🟢 Соединение с базой данных успешно установленно\n'
                               f'Пожалуйста, выберите формат отчета 👇',
                               reply_markup=report_markup
                               )
    else:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=check_db_con_message.message_id)
        await bot.send_message(callback.from_user.id,
                               f'🔴 Не удалось установить соединение с базой данных\n'
                               f'Пожалуйста, попробуйте позже.',
                               )
