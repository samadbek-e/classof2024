from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def alumnisIDSelectorButtons():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=f"{i + j * 8 + 1}", callback_data=f"{i + j * 8 + 1}") for i in range(8)] for j in range(10)
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Choose ID of the person you want to wish",
    selective=True
    )