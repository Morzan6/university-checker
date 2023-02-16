import sys
import os
sys.path.append('../../')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from aiogram import Bot, Dispatcher, executor, types
from config.settings import TOKEN, admin_id  #Админ id из токен файла, можно добавить нескольно, чтобы бот при старте писал админу, что запущен и т. д.
from tgbot.keyboard import main_markup
#from tgbot.add_remove_service import add_service, remove_service
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from models.models import Service 
from models.models import User
import base64
#библиотечки

bot = Bot(TOKEN)
dp = Dispatcher(bot)


HelpStart = 'Здравствуйте, бот присылает уведомления о состонии сервисов Российских ВУЗов' + '\n\nДля работы с ботом вам необходимо зарегистрироваться на сайте по этой ссылке:\n' #Текст при команде start/help + добавить описание команд

async def confirm_url(User_id):
    User_id = str(User_id)
    base64_user_id = base64.b64encode(bytes(User_id, 'utf-8')).decode('utf-8')
    return f'university-checker.ru/activatetg&{base64_user_id}'



async def on_startup(_): #Функция при запуске бота
    await bot.send_message(admin_id, text='Bot has been started') #Отправка сообщения админу
    #await bot.send_message(596742400, text='Bot has been started')
    #sql_start() тут подключение к БД





async def main_msg_add(User_id):
    message_add = 'Выберите ниже вуз, на сервис которого хотите подписаться \n\n'
    for obj in Service.objects.all():
        message_add += '<a href=' +  '"' + "university-checker.ru/add_subscribe&" + obj.slug + '"' + '>'+ obj.name + '</a>' + '\n\n'
    await bot.send_message(User_id, message_add, parse_mode=types.ParseMode.HTML)



async def get_values_by_column(User_id):
    queryset = User.objects.all()
    filtered_queryset = queryset.filter(**{'tgid': User_id})
    model_obj = filtered_queryset.first()
    value = getattr(model_obj, 'subscribes')
    value_list = [s.strip() for s in value.split(',')] if value else []
    return value_list


async def main_msg_delete(User_id):
    message_remove = 'Выберите ниже вуз, от сервиса которого хотите отписаться \n\n'
    slugs = await get_values_by_column(User_id)
    slugs.pop()
    for slug in slugs:
        service = Service.objects.get(slug = slug)
        message_remove += '<a href=' +  '"' + "university-checker.ru/remove_subscribe&" + slug + '"' + '>'+ service.name + '</a>' + '\n\n'
    await bot.send_message(User_id, message_remove, parse_mode=types.ParseMode.HTML)
    




#Обработка команд бота
@dp.message_handler(commands=['help', 'start', 'addService', 'removeService'])
async def commands(message: types.Message):
    if message.text == '/help':
        await message.answer(HelpStart + await confirm_url(message.from_user.id),  parse_mode='HTML', reply_markup=main_markup)
        #await message.answer(await confirm_url(message.from_user.id), parse_mode='HTML', reply_markup=main_markup)
    elif message.text == '/start':
        await message.answer(HelpStart + await confirm_url(message.from_user.id), parse_mode='HTML', reply_markup=main_markup)


# @dp.callback_query_handler() #Обработка запросов
# async def callback(callback: types.CallbackQuery):
#     if callback.data in addWeb: #добавляет сервис
#         user_login = str(callback.from_user.id)
#         service = str(callback.data)
#         print(user_login, service)
#         first_name = str(callback.from_user.first_name) #данные о пользователе, можно удалять крч
#         user_name = str(callback.from_user.username) #данные о пользователе, можно удалять крч
#         last_name = str(callback.from_user.last_name) #данные о пользователе, можно удалять крч
#         await add_service(user_login, service)
#         await bot.send_message(callback.from_user.id, 'Сервис добавлен')
#     elif callback.data in addWeb_remove: #Удаляет сервис
#         user_login = str(callback.from_user.id)
#         service = str(callback.data)
#         print(user_login, service)
#         first_name = str(callback.from_user.first_name) #данные о пользователе, можно удалять крч
#         user_name = str(callback.from_user.username) #данные о пользователе, можно удалять крч
#         last_name = str(callback.from_user.last_name) #данные о пользователе, можно удалять крч
#         await remove_service(user_login, service)
#         await bot.send_message(callback.from_user.id, 'Сервис удален')

@dp.callback_query_handler() #Обработка запросов
async def callback(callback: types.CallbackQuery):
    if callback.data == 'addss':
        if User.objects.filter(tgid='my_value').exists():
            await main_msg_add(callback.from_user.id)
        else:
            await bot.send_message(callback.from_user.id, 'Извините, кажется, что ваш telegram аккаунт не привязан к аккаунту на нашем сайте, чтобы это исправить перейдите по ссылке и авторизируйтесь или зарегистрируйтесь\n\n' + str(await confirm_url(callback.from_user.id)))
    if callback.data == 'removess':
        if User.objects.filter(tgid='my_value').exists():
            await main_msg_delete(callback.from_user.id)
        else:
            await bot.send_message(callback.from_user.id, 'Извините, кажется, что ваш telegram аккаунт не привязан к аккаунту на нашем сайте, чтобы это исправить перейдите по ссылке и авторизируйтесь или зарегистрируйтесь\n\n' + str(await confirm_url(callback.from_user.id)))

async def notification(service_slug, error_code): # Оповещает о неработе сервиса
    # notif = 'Внимание, сервис ' + str(service) + ' не работает' #Можно добавить условие на ddos, краш и другие ошибки
    # for i in range(len(user_logins)):
    #     await bot.send_message(user_logins[i], notif)
    users = User.objects.filter(subscribes__icontains = service_slug)
    service = Service.objects.get(slug = service_slug)
    for user in users:
        print(user.tgid)
        print(service.name)
        if user.tgid != None:
            notif = 'Внимание, обнаружена ошибка в работе сервиса: ' + str(service.name) + "\n\nОшибка: " + str(error_code) + '\n\nСсылка на сервис - ' + str(service.url)
            await bot.send_message(user.tgid, notif)




if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
