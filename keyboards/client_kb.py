from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# --- Клавиатура для главного меню ---
create_report = InlineKeyboardButton(text='Отчет',
                                     callback_data='/report')

menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [create_report],
    ]
)

back_to_menu = KeyboardButton(text='/start_menu')
to_menu = ReplyKeyboardMarkup(
    keyboard=[
        [back_to_menu]
    ],
    resize_keyboard=True,
)

# --- Клавиатура для /report callback ---
last_day_report = InlineKeyboardButton(text='За последний день',
                                       callback_data='/last_day_report')
last_month_report = InlineKeyboardButton(text='За последний месяц',
                                         callback_data='/last_month_report')
last_year_report = InlineKeyboardButton(text='За последний год',
                                        callback_data='/last_year_report')

report_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [last_day_report],
        [last_month_report],
        [last_year_report],
    ]
)
