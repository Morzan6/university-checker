from aiogram import Bot, Dispatcher, executor, types
from configtg import TOKEN, admin_id  #Админ id из токен файла, можно добавить нескольно, чтобы бот при старте писал админу, что запущен и т. д.
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3 as sq
#библиотечки
import os, django
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

   #Убрать токен отсюда, добавить в cfg файл


bot = Bot(TOKEN)
dp = Dispatcher(bot)
#токен бота из config файла импортировать



#основные кнопки
markupweb = InlineKeyboardMarkup(row_width=1)
web_mpti = types.InlineKeyboardButton('mpti', callback_data = 'mpti')
web_bmstu = types.InlineKeyboardButton('bmstu', callback_data = 'bmstu')
#Добавить сюда все сервисы


markupweb.add(web_mpti, web_bmstu) #Добавить все сайты сюда
addWeb = ['mpti', 'bmtsu'] #нужно для оптимизации кода(не 100 if, а проверка значения сайта на вхождение в список), добавить сюда все вузы


#Remove кнопки
markupweb_remove = InlineKeyboardMarkup(row_width=1)
web_mpti_remove = types.InlineKeyboardButton('mpti', callback_data = 'mpti_remove')
web_bmstu_remove = types.InlineKeyboardButton('bmstu', callback_data = 'bmstu_remove')
#Добавить сюда все сервисы

markupweb_remove.add(web_mpti_remove, web_bmstu_remove) #Добавить сюда все remove кнопки
addWeb_remove = ['mpti_remove', 'bmstu_remove']





async def on_startup(_): #Функция при запуске бота
    await bot.send_message(admin_id, text='Bot has been started') #Отправка сообщения админу
    #sql_start() тут подключение к БД


HelpStart = 'Здравствуйте, бот присылает уведомления о состонии сервисов Российских ВУЗов'  #Текст при команде start/help + добавить описание команд
#Обработка команд бота
@dp.message_handler(commands=['help', 'start', 'addServices', 'removeService']) 
async def commands(message: types.Message):
    if message.text == '/help':
        await message.answer(HelpStart, parse_mode='HTML', reply_markup=markupweb)
    elif message.text == '/start':
        await message.answer(HelpStart, parse_mode = 'HTML', reply_markup=markupweb)
    elif message.text =='/addServices':
        await message.answer('Выберите сервисы, которые нужно добавить для оповещения', parse_mode='HTML', reply_markup=markupweb)
    elif message.text =='/removeService':
        await message.answer('Выберите сервисы, которые нужно удалить из оповещения', parse_mode='HTML', reply_markup=markupweb_remove)


@dp.callback_query_handler() #Обработка запросов
async def callback(callback: types.CallbackQuery):
    if callback.data in addWeb: #добавляет сервис 
        user_login = str(callback.from_user.id)
        service = str(callback.data)
        print(user_login, service)
        first_name = str(callback.from_user.first_name) #данные о пользователе, можно удалять крч
        user_name = str(callback.from_user.username) #данные о пользователе, можно удалять крч
        last_name = str(callback.from_user.last_name) #данные о пользователе, можно удалять крч
        add_service(user_login, service)
        await bot.send_message(callback.from_user.id, 'Сервис добавлен')
    elif callback.data in addWeb_remove: #Удаляет сервис
        user_login = str(callback.from_user.id)
        service = str(callback.data)
        print(user_login, service)
        first_name = str(callback.from_user.first_name) #данные о пользователе, можно удалять крч
        user_name = str(callback.from_user.username) #данные о пользователе, можно удалять крч
        last_name = str(callback.from_user.last_name) #данные о пользователе, можно удалять крч
        remove_service(user_login, service)
        await bot.send_message(callback.from_user.id, 'Сервис удален')



async def add_service(user_login, service):  #Добавляет сервис
    pass

async def remove_service(user_login, service): #Удаляет сервис
    pass

async def notification(user_logins, service): #Оповещает о неработе сервиса
    notif = 'Внимание, сервис' + str(service) + 'не работает' #Можно добавить условие на ddos, краш и другие ошибки
    pass




if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
