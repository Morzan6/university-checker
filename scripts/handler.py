"""
Чтобы запустить скрипт в терминале прописать "python  scripts/handler.py" (без кавычек)
"""
import requests

import threading
import asyncio
#просто настройки джанги
import requests
import time
from datetime import datetime, timezone, timedelta
import os, django
import sys
sys.path.append('../../')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

#импорт модели сервиса
from models.models import Service
from models.models import User
from tgbot.main import notification
from scripts.sending import email_alert


timezone_offset = 3.0  
tzinfo = timezone(timedelta(hours=timezone_offset))

#полчаем массив со словарями в переменной Dict формата [{'name': 'МФТИ', 'url': 'https://mipt.ru/'}, {'name': 'МГТУ им. Н. Э. Баумана', 'url': 'https://bmstu.ru/'}...]
Dict = Service.objects.values("name", "url","slug")
print(Dict)

async def DDoS_checker():
    while True:
        for service in Dict:
            url = service['url']
            print(url)
            response = requests.get(url) 
            print(response.elapsed.total_seconds())
            if response.elapsed.total_seconds() > 30:
                print('DDoS')
            if response.elapsed.total_seconds() > 30:
              await email_alert(service.slug,100)
            

            if response.elapsed.total_seconds() > 30:
                service = Service.objects.get(url=url)
                status = service.status
                status = status + " " + str("100") + ","
                service.status = status

                reports = service.reports
                reports = reports + " |"
                service.reports = reports

                current_time = service.time
                current_time = current_time + " "+ str(datetime.now().replace(microsecond=0))+","
                service.time = current_time

                service.save()
                

            time.sleep(10)
        await asyncio.sleep(1)

async def error_codes():
    while True:
        for service in Dict:
            url = service['url']
            response = requests.get(f"{url}", timeout=5)
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
            #if response.status_code >= 300:
        time.sleep(10)      
        await notification('bmstu', 'Ddos')
        await asyncio.sleep(1) 

# t1 = threading.Thread(target=DDoS_checker)
# t2 = threading.Thread(target=error_codes)
# t1.start()
# t2.start()
# async def main():
#     t1 = asyncio.create_task(DDoS_checker())
#     t2 = asyncio.create_task(error_codes())
#     await t2
#     await t1

# asyncio.run(main())
async def main():
    await asyncio.gather(error_codes(),DDoS_checker())

asyncio.run(main())


# await notification([975083397],'Университет имени Баумэна') Добавить куда надо, аргументами список с юзерами, в строку slug/сразу название вуза 

