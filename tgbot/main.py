from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, admin_id  #Админ id из токен файла, можно добавить нескольно, чтобы бот при старте писал админу, что запущен и т. д.
from keyboard_ import markupweb, markupweb_remove, addWeb, addWeb_remove
from add_remove_service import add_service, remove_service
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



async def notification(user_logins, service): # Оповещает о неработе сервиса
    notif = 'Внимание, сервис' + str(service) + 'не работает' #Можно добавить условие на ddos, краш и другие ошибки
    for i in range(len(user_logins)):
        await bot.send_message(user_logins[i], notif)



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
