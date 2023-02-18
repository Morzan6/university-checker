from aiogram import types
from aiogram.types import InlineKeyboardMarkup


# основные кнопки
markupweb = InlineKeyboardMarkup(row_width=1)
web_mpti = types.InlineKeyboardButton('mpti', callback_data = 'mpti')
web_bmstu = types.InlineKeyboardButton('bmstu', callback_data = 'bmstu')
# Добавить сюда все сервисы


markupweb.add(web_mpti, web_bmstu) # Добавить все сайты сюда
addWeb = ['bmstu', 'mpti']  # нужно для оптимизации кода(не 100 if, а проверка значения сайта на вхождение в список),
# добавить сюда все вузы






# Remove кнопки
markupweb_remove = InlineKeyboardMarkup(row_width=1)
web_mpti_remove = types.InlineKeyboardButton('mpti', callback_data = 'mpti_remove')
web_bmstu_remove = types.InlineKeyboardButton('bmstu', callback_data = 'bmstu_remove')
# Добавить сюда все сервисы

markupweb_remove.add(web_mpti_remove, web_bmstu_remove) # Добавить сюда все remove кнопки
addWeb_remove = ['mpti_remove', 'bmstu_remove']


# add_service
main_markup = InlineKeyboardMarkup(row_width=1)
main_markup_add = types.InlineKeyboardButton('Добавить вуз в избранное', callback_data = 'addss')
main_markup_remove = types.InlineKeyboardButton('Посмотреть избранное', callback_data = 'removess')
main_markup.add(main_markup_add, main_markup_remove)