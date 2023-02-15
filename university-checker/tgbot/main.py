import sys
import os
sys.path.append('../../')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from aiogram import Bot, Dispatcher, executor, types
from config.settings import TOKEN, admin_id  #Админ id из токен файла, можно добавить нескольно, чтобы бот при старте писал админу, что запущен и т. д.
from tgbot.keyboard import markupweb, markupweb_remove, addWeb, addWeb_remove
from tgbot.add_remove_service import add_service, remove_service

from models.models import Service 
from models.models import User
#библиотечки

bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def on_startup(_): #Функция при запуске бота
    await bot.send_message(admin_id, text='Bot has been started') #Отправка сообщения админу
    #sql_start() тут подключение к БД


HelpStart = 'Здравствуйте, бот присылает уведомления о состонии сервисов Российских ВУЗов'  #Текст при команде start/help + добавить описание команд
#Обработка команд бота
@dp.message_handler(commands=['help', 'start', 'addService', 'removeService'])
async def commands(message: types.Message):
    if message.text == '/help':
        await message.answer(HelpStart, parse_mode='HTML', reply_markup=markupweb)
    elif message.text == '/start':
        await message.answer(HelpStart, parse_mode='HTML', reply_markup=markupweb)
    elif message.text =='/addService':
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
        await add_service(user_login, service)
        await bot.send_message(callback.from_user.id, 'Сервис добавлен')
    elif callback.data in addWeb_remove: #Удаляет сервис
        user_login = str(callback.from_user.id)
        service = str(callback.data)
        print(user_login, service)
        first_name = str(callback.from_user.first_name) #данные о пользователе, можно удалять крч
        user_name = str(callback.from_user.username) #данные о пользователе, можно удалять крч
        last_name = str(callback.from_user.last_name) #данные о пользователе, можно удалять крч
        await remove_service(user_login, service)
        await bot.send_message(callback.from_user.id, 'Сервис удален')



async def notification(service_slug, error_code): # Оповещает о неработе сервиса
    # notif = 'Внимание, сервис ' + str(service) + ' не работает' #Можно добавить условие на ddos, краш и другие ошибки
    # for i in range(len(user_logins)):
    #     await bot.send_message(user_logins[i], notif)
    users = User.objects.filter( subscribes__icontains = service_slug )
    service = Service.objects.get(slug = service_slug)
    for user in users:
        print(user.tgid)
        print(service.name)
        notif = 'Внимание, обнаружена ошибка в работе сервиса: ' + str(service.name) + "\n\nОшибка: " + str(error_code) + '\n\nСсылка на сервис - ' + str(service.url)
        await bot.send_message(user.tgid, notif)




if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)