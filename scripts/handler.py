"""
Чтобы запустить скрипт в терминале прописать "python  scripts/handler.py" (без кавычек)
"""
import requests
import datetime 
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
        time.sleep(10)
DDoS_checker()



###