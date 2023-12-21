from create_bot import dp, bot, spark
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto, FSInputFile
from keyboards.client_kb import menu_markup, to_menu, report_markup
from reports import report_maker


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


@dp.callback_query(lambda callback: callback.data in ['/last_day_report'])
async def last_day_report_builder(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.answer()

    wait_message = await bot.send_message(callback.from_user.id,
                                          f'Пожалуйста, подождите.\n'
                                          f'Идет формирование отчета...\nПримерное время ожидания - 4 мин',
                                          reply_markup=to_menu
                                          )

    rep = report_maker.ReportGenerator(spark.get_table('orders'),
                                       spark.get_table('products'),
                                       spark.get_table('buyers'))

    charts_names = rep.create_last_day_report()
    media = [InputMediaPhoto(media=FSInputFile(f'./data/charts/{chart_name}')) for chart_name in charts_names]

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=wait_message.message_id)

    await bot.send_media_group(callback.message.chat.id, media)
    await bot.send_message(callback.from_user.id,
                           f'Вот ваш отчет за последний день.'
                           )
