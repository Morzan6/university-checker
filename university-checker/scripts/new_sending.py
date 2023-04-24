import os, django
import sys
sys.path.append('../../')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from models.models import Service
from models.models import User
from tgbot.notifdef import notification, good_notification
from scripts.sending import email_alert, good_email_alert
import asyncio



Dict = Service.objects.values("slug","status")
for el in Dict:
    el["status"] = el["status"].split(', ')
    for i in range(len(el["status"])):
        el["status"][i] = el["status"][i].replace(' ', '')
        el["status"][i] = el["status"][i].replace(',', '')
        el['status'][i] = int(el["status"][i])
print(Dict)


async def new_sending():
    for service in Dict:
        slug = service['slug']
        codes = service['status']
        if len(codes) <= 1 and codes[-1] >= 300:
            await email_alert(slug, codes[-1])
            await notification(slug, codes[-1])
        elif codes[-2] < 300 and codes[-1] >= 300:
            await email_alert(slug, codes[-1])
            await notification(slug, codes[-1])
        elif codes[-2] > 300 and codes[-1] < 300:
            await good_email_alert(slug, codes[-1])
            await good_notification(slug, codes[-1])
