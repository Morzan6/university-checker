"""
Чтобы запустить скрипт в терминале прописать "python  scripts/handler.py" (без кавычек)
"""
import requests
import datetime
import threading
import asyncio
#просто настройки джанги
import requests
import time
import datetime 
import os, django
import sys
sys.path.append('../../')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

#импорт модели сервиса
from services_model.models import Service
from user_model.models import User
from tgbot.main import notification

#полчаем массив со словарями в переменной Dict формата [{'name': 'МФТИ', 'url': 'https://mipt.ru/'}, {'name': 'МГТУ им. Н. Э. Баумана', 'url': 'https://bmstu.ru/'}...]
Dict = Service.objects.values("name", "url")
print(Dict)

def DDoS_checker():
    while True:
        for service in Dict:
            url = service['url']
            print(url)
            response = requests.get(url) 
            print(response.elapsed.total_seconds())
            if response.elapsed.total_seconds() > 30:
                print('DDoS')


            service = Service.objects.get(url=url)
            status = service.status
            status = status + " " + str(response.elapsed.total_seconds()) + ","
            service.status = status

            reports = service.reports
            reports = reports + " |"
            service.reports = reports

            current_time = service.time
            current_time = current_time + " "+ str(datetime.datetime.now())+","
            service.time = current_time

            service.save()

        time.sleep(10)

def error_codes():
    while True:
        for service in Dict:
            url = service['url']
            response = requests.get(f"{url}", timeout=0.5)
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
            current_time = current_time + " "+ str(datetime.datetime.now())+","
            service.time = current_time

            service.save()
            
            #if response.status_code >= 300:
        time.sleep(10)       
        


t1 = threading.Thread(target=DDoS_checker)
t2 = threading.Thread(target=error_codes)
t1.start()
t2.start()