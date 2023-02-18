from aiogram import types
from aiogram.types import InlineKeyboardMarkup
#библиотеки


#Основные кнопки бота
main_markup = InlineKeyboardMarkup(row_width=1)
main_markup_add = types.InlineKeyboardButton('Добавить вуз в избранное', callback_data = 'addss')
main_markup_remove = types.InlineKeyboardButton('Посмотреть избранное', callback_data = 'removess')
main_markup.add(main_markup_add, main_markup_remove)