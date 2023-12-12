from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# --- Клавиатура для главного меню ---
create_report = InlineKeyboardButton(text='Отчет',
                                     callback_data='/report')

menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [create_report],
    ]
)