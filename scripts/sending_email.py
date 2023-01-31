import os, django
import sys 
sys.path.append('../../')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()



from services_model.models import Service 
from user_model.models import User
from django.core.mail import EmailMessage

def email_alert(service_slug,Error):
    users = User.objects.filter( subscribes__icontains = service_slug )
    service = Service.objects.get(slug = service_slug)
    print(service.name)
    for user in users:

        email = EmailMessage(f'{service.name}-Сбой в работе сервиса {service.url}', f'Внимание замечен сбой в {service.url} ', to=[user.email])
        email.send() #Написать более объемное предложение
email_alert('mpti',200)        