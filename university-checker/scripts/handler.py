"""
Чтобы запустить скрипт в терминале прописать "python  scripts/handler.py" (без кавычек)
"""
import requests

import threading
import asyncio
#просто настройки джанги
import requests
from requests.exceptions import Timeout
import time
from datetime import datetime, timezone, timedelta
import os, django
import sys
sys.path.append('../../')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

#импорт модели сервиса
from scripts.new_sending import new_sending
from models.models import Service
from models.models import User
from tgbot.notifdef import notification
from scripts.sending import email_alert


timezone_offset = 3.0  
tzinfo = timezone(timedelta(hours=timezone_offset))

#полчаем массив со словарями в переменной Dict формата [{'name': 'МФТИ', 'url': 'https://mipt.ru/'}, {'name': 'МГТУ им. Н. Э. Баумана', 'url': 'https://bmstu.ru/'}...]
Dict = Service.objects.values("name", "url","slug")
print(Dict)

# async def DDoS_checker():
#     while True:
#         for service in Dict:
#             url = service['url']
#             print(url)
#             try:
#                 response = requests.get(url, timeout=35)
#                 print(response.elapsed.total_seconds())
#             except Timeout:
#                 print('DDoS')
#                 # await email_alert(service['slug'], 100)
#                 # await notification(service['slug'], 100)
#                 print(f'Request timed out for {url}')               

#         time.sleep(10)
#         await asyncio.sleep(1)

async def error_codes():
    while True:
        for service in Dict:
            url = service['url']
            print(url)
            slug = service['slug']
            try:
                response = requests.get(f"{url}", timeout=35)
                print(response.elapsed.total_seconds())
            except Timeout:
                print('DDoS')
                print(f'Request timed out for {url}')
                service = Service.objects.get(url=url)
                status = service.status
                status = status + " " + "100" + ","
                service.status = status

                reports = service.reports
                reports = reports + " |"
                service.reports = reports

                current_time = service.time
                current_time = current_time + " "+ str(datetime.now().replace(microsecond=0))+","
                service.time = current_time

                service.save()
            code = response.status_code
            print("Code:", code)

            #добавляет в БД все что надо
            service = Service.objects.get(url=url)
            status = service.status
            status = status + " " + str(code) + ","
            service.status = status

            reports = service.reports
            reports = reports + " |"
            service.reports = reports

            current_time = service.time
            current_time = current_time + " "+ str(datetime.now().replace(microsecond=0))+","
            service.time = current_time

            service.save()
            await new_sending()
            
        time.sleep(1200)      
        await asyncio.sleep(1) 

async def main():
    await asyncio.gather(error_codes())


if __name__ == "__main__":
    asyncio.run(main())
