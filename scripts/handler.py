"""
Чтобы запустить скрипт в терминале прописать "python  scripts/handler.py" (без кавычек)
"""

#просто настройки джанги
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

def site_up():
    for service in Dict:
        url = service['url']
        print(url)

site_up()

