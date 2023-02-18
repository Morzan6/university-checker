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
#Подключение библиотек и импортирование модулей из других файлов

#Создание самого бота
bot = Bot(TOKEN)
dp = Dispatcher(bot)


#Функция возвращающая ссылку, к которой привязан телеграм id, при переходе по ссылке телеграм аккаунт автоматически привяжется к аккаунту на сайте
async def confirm_url(User_id):
    User_id = str(User_id)
    base64_user_id = base64.b64encode(bytes(User_id, 'utf-8')).decode('utf-8')
    return f'university-checker.ru/activatetg&{base64_user_id}'


#Запускает бота и уведомляет админа о том, что бот запущен(admin_id берется из university-checker/university-checker/config/settings.py)
async def on_startup(_):
    await bot.send_message(admin_id, text='Bot has been started')

#Функция нужна для генерации и отправки сообщения,в котором есть гиперссылка на подключение аккаунта телеграм к аккаунту на сайте 
async def HelpStart(User_id):
    print(User_id)
    await bot.send_message(User_id, f'Здравствуйте, бот присылает уведомления о состонии сервисов Российских ВУЗов🏛️ \n\nДля работы с ботом <a href= "{str(await confirm_url(User_id))}">привяжите</a> telegram аккаунт к аккаунту на сайте\n\nВы также можете посетить <a href= "https://university-checker.ru/">наш сайт</a> ', parse_mode=types.ParseMode.HTML, reply_markup=main_markup)
    


# получает вузы из бд и отправляет сообщение, в котором есть все вузы в виде гиперссылки, которая активирует функцию на сайте, которая добавляет вуз в избранное
async def main_msg_add(User_id):
    message_add = 'Выберите ниже вуз🏛️, на сервис которого хотите подписаться \n\n'
    for obj in Service.objects.all():
        message_add += '<a href=' +  '"' + "university-checker.ru/add_subscribe&" + obj.slug + '"' + '>'+ '• '+obj.name + '</a>' + '\n\n'

    max_message_length = 4096
    current_length = 0
    message_parts = []
    current_part = ''

    for line in message_add.split('\n'):
        if current_length + len(line) + 1 > max_message_length:
            message_parts.append(current_part)
            current_part = ''
            current_length = 0
        current_part += line + '\n'
        current_length += len(line) + 1

    message_parts.append(current_part)

    for i, part in enumerate(message_parts):
        if i > 0 or len(message_parts) > 1:
            part = '\n' + part

        if i == len(message_parts) - 1:
            await bot.send_message(User_id, part, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True, reply_markup=main_markup)
        else:
            await bot.send_message(User_id, part, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)





        



# Функция получает список вузов, на которые подписан пользватель по его ID в телегам
async def get_values_by_column(User_id):
    queryset = User.objects.all()
    filtered_queryset = queryset.filter(**{'tgid': User_id})
    model_obj = filtered_queryset.first()
    value = getattr(model_obj, 'subscribes')
    value_list = [s.strip() for s in value.split(',')] if value else []
    return value_list

# получает вузы из бд и отправляет сообщение, в котором есть все вузы, на которые подписан пользователь, в виде гиперссылки, которая активирует функцию на сайте, которая удаляет вуз из избранного
async def main_msg_delete(User_id):
    message_remove = 'Список вузов🏛️, на которые вы подписаны, при проблеме в работе сервиса одного из них вы будете получать уведомление🔔.\n\n\nВы также можете удалить вуз🏛️, перейдя по гиперссылке \n\n\n'
    slugs = await get_values_by_column(User_id)
    test123 = ['']
    print(slugs)
    if slugs != test123:
        del slugs[-1]
        for slug in slugs:
            service = Service.objects.get(slug = slug)
            # message_remove += '<a href=' +  '"' + "university-checker.ru/delete_subscribe&" + slug + '"' + '>'+ '• '+service.name + '</a>' + '\n\n'
            message_remove += '• '+'<b>'+service.name+'</b>' + '<a href=' + '"' + "university-checker.ru/delete_subscribe&" + slug + '"' + '>' + "\nУДАЛИТЬ" +  '</a>' + '\n\n\n'
        #await bot.send_message(User_id, message_remove, parse_mode=types.ParseMode.HTML)
    else:
        message_remove = 'Вы не подписаны ни на один вуз🏛️!'
    max_message_length = 4096
    current_length = 0
    message_parts = []
    current_part = ''


    if message_remove != 'Вы не подписаны ни на один вуз🏛️!':
        for line in message_remove.split('\n\n'):
            if current_length + len(line) + 1 > max_message_length:
                message_parts.append(current_part)
                current_part = ''
                current_length = 0
            current_part += line + '\n'
            current_length += len(line) + 1

        message_parts.append(current_part)

        for i, part in enumerate(message_parts):
            if i > 0 or len(message_parts) > 1:
                part = '\n' + part

            if i == len(message_parts) - 1:
                await bot.send_message(User_id, part, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True, reply_markup=main_markup)
            else:
                await bot.send_message(User_id, part, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
    else:
        await bot.send_message(User_id, message_remove)
    




#Обработка команд бота
@dp.message_handler(commands=['help', 'start'])
async def commands(message: types.Message):
    if message.text == '/help':
        await HelpStart(message.from_user.id)
    elif message.text == '/start':
        await HelpStart(message.from_user.id)



#Обработка запросов с проверкой, связал ли пользователь аккаунт тг с аккаунтом на сайте
@dp.callback_query_handler()
async def callback(callback: types.CallbackQuery):
    if callback.data == 'addss':
        if User.objects.filter(tgid=callback.from_user.id).exists():
            await main_msg_add(callback.from_user.id)
        else:
            #                                                                                                                                            message_remove += '<a href=' +  '"' + "university-checker.ru/delete_subscribe&" + slug + '"' + '>'+ service.name + '</a>' + '\n\n'
            await bot.send_message(callback.from_user.id, f'Извините, кажется, что ваш telegram аккаунт <u>не привязан</u> к аккаунту на нашем сайте, чтобы это исправить <a href= "{str(await confirm_url(callback.from_user.id))}">привяжите аккаунт</a>, для этого нужно сначала авторизироваться' , parse_mode=types.ParseMode.HTML)
    if callback.data == 'removess':
        if User.objects.filter(tgid=callback.from_user.id).exists():
            await main_msg_delete(callback.from_user.id)
        else:
            await bot.send_message(callback.from_user.id, f'Извините, кажется, что ваш telegram аккаунт <u>не привязан</u> к аккаунту на нашем сайте, чтобы это исправить <a href= "{str(await confirm_url(callback.from_user.id))}">привяжите аккаунт</a>, для этого нужно сначала авторизироваться' , parse_mode=types.ParseMode.HTML)


# Функция оповещения пользователя о неработающем сервисе и ошибке, отправляет только тем пользователям, которые подписаны на сервис
async def notification(service_slug, error_code):
    users = User.objects.filter(subscribes__icontains = service_slug)
    service = Service.objects.get(slug = service_slug)
    for user in users:
        print(user.tgid)
        print(service.name)
        if user.tgid != None:
            notif = '⚠️обнаружена ошибка в работе сервиса: ' + str(service.name) + "\n\nОшибка " + str(error_code) + ': '+ str(Dict_error[error_code]) + '\n\nСсылка на сервис - ' + str(service.url)
            await bot.send_message(user.tgid, notif)


# Словарь с расшифровкой кодов ошибок
Dict_error={
    '100':'Возможна DDoS атака',
    '300': 'Затребованный url обозначает более одного ресурса, и сервер не смог однозначно определить, к какой странице url относится.',
    '301': 'Документ уже не используется сервером, а ссылка перенаправляет на другую страницу.',
    '303': 'Запрошенный ресурс находится под другим адресом и его следует запрашивать.',
    '305': 'Доступ к затребованному ресурсу может осуществляться только через прокси-сервер,',
    '307': 'Требуемый ресурс был временно переведен на другой адрес.',
    '308': 'Документ уже не используется сервером.',
    '400': 'Неверный запрос. В запросе есть синтаксическая ошибка,по причине этого запрос не может быть выполнен. Пожалуйста перепроверьте url-адрес сайта.',
    '401': 'Для доступа на эту страницу требуется авторизация на сервере.',
    '402': 'Внутренняя ошибка или ошибка конфигурации сервера.',
    '403': 'Доступ запрещён. Администратор сервера ограничил доступ к ресурсу.',
    '404': 'Страница,которую вы запросили,не найдена на сервере,по причине того,что она была удалена и более не существует.',
    '405': 'Метод, определенный в строке запроса, не дозволено применять для указанного ресурса, поэтому сервер не смог его проиндексировать.',
    '406': 'Нужный документ существует, но не в том формате.',
    '407': 'Необходима регистрация на прокси-сервере.',
    '408': 'Время запроса истекло. Пожалуйста проверьте ваше интернет-соединение. Или подождите,сайт может быть перегружен на данный момент времени.',
    '409': 'Запрос конфликтует с другим запросом или с конфигурацией сервера.',
    '410': 'Страница более не существует. Указанный url-адрес верен и не содержит ошибок,но страница была удалена.',
    '412': 'При проверке на сервере одного или более полей заголовка запроса обнаружено несоответствие.',
    '413':'Размер запроса больше, чем сервер может обоработать.',
    '414': 'Сервер отказывается обслуживать запрос, потому что запрашиваемый сервером url длиннее, чем сервер может интерпретировать.',
    '415': 'Сервер отказывается обрабатывать запрос, потому что тело запроса имеет неподдерживаемый формат.',
    '422': 'Сервер не в состоянии обработать один (или более) элемент запроса.',
    '423': 'Сервер отказывается обработать запрос, так как один из требуемых ресурсов заблокирован.',
    '424': 'Сервер отказывается обработать запрос, так как один из зависимых ресурсов заблокирован.',
    '426': 'Сервер запросил апгрейд соединения до SSL, но SSL не поддерживается клиентом.',
    '429':'Вами было отправлено слишком много запрос за короткий период времени.',
    '500': 'Внутренняя ошибка сервера.',
    '502': 'Сервер, действуя в качестве шлюза или прокси-сервера, получил недопустимый ответ от следующего сервера в цепочке запросов, к которому обратился при попытке выполнить запрос.',
    '503': 'Сервис недоступен. Возникла ошибка из-за временной перегрузки или отключения на техническое обслуживание сервера.',
    '504': 'Сервер, при работе в качестве внешнего шлюза или прокси-сервера, своевременно не получил отклик от вышестоящего сервера, к которому он обратился, пытаясь выполнить запрос.',
    '505': 'Сервер не поддерживает или отказывается поддерживать версию HTTP-протокола, которая используется в сообщении запроса робота.',
    '507': 'Сервер не может обработать запрос из-за недостатка места на диске.'
}

# запуск Бота
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
