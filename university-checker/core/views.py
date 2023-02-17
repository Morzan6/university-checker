from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import  authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from scripts.tokens import account_activation_token
from scripts.handle_image import handle_uploaded_file
from models.models import Service
from models.models import Report
from models.models import Raiting
from transliterate import translit
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import datetime, timezone, timedelta
import re
import urllib.parse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.datastructures import MultiValueDictKeyError
import base64
from scripts.time_delta import time_dif

User = get_user_model()

def count_services():
    count = Service.objects.all().count()
    
    return count

def func_chunk(lst, n):
    for x in range(0, len(lst), n):
        e_c = lst[x : n + x]

        if len(e_c) < n:
            e_c = e_c + [None for y in range(n - len(e_c))]
        yield e_c



    

#обработчик главной страницы
def index(request):
    services = Service.objects.all()[:5]

    full_array = []
    for s in services:
        service = Service.objects.get(slug=s.slug)
        
        all_info = []

        time = (service.time).split(",")
        time = [i[:].strip() for i in time]
        del time[-1]

        for t in time:
            datetime_dict = {}
            time_ = t[11:]
            date = t[:-9]
            datetime_dict['year'] = int(date[:-6])
            datetime_dict['month'] = int(date[5:-3])
            datetime_dict['day'] = int(date[8:])
            datetime_dict['hour'] = int(time_[:-6])
            datetime_dict['minute'] = int(time_[3:-3])
            datetime_dict['second'] = int(time_[6:])
            
            all_info.append(datetime_dict)
       
        
    
        status = (service.status).split(",")
        del status[-1]
        
        status = [int(i.strip()) for i in status]

        for s in range(len(status)):
            if status[s] >= 200 and status[s] < 300:
                status[s] = 1
            elif status[s] >= 500 and status[s] < 600:
                status[s] = 20
            elif status[s] >= 400 and status[s] < 500:
                status[s] = 15
            elif status[s] >= 300 and status[s] < 400:
                status[s] = 5
            elif status[s] >= 100 and status[s] < 200:
                status[s] = 10

        reports = (service.reports).split("|")
        
        delta = time_dif(f"{all_info[-1]['year']}-{all_info[-1]['month']}-{all_info[-1]['day']} {all_info[-1]['hour']}:{all_info[-1]['minute']}:{all_info[-1]['second']}")

        for i in all_info:
            i['delta'] = delta

        count_rep = []
        for report in reports:
            report = report.split(",")
            reports_count = len(report)
            count_rep.append(reports_count)
        

        incedents = [a*b*(-1) for a,b in zip(count_rep,status)]
    

        for dt, i in zip(all_info, incedents):
            dt['y'] = i
        
        for inf in all_info:
            inf['name'] = service.name
            inf['slug'] = service.slug
            
               
        #Удаляем все значения которые были раньше чем ближайшие 24 часа 
        for item in list(all_info):
            datetime_ = datetime.strptime(f"{item['year']}-{item['month']}-{item['day']} {item['hour']}:{item['minute']}:{item['second']}", "%Y-%m-%d %H:%M:%S")
            
            compare = datetime.now().replace(microsecond=0)
            compare -= timedelta(days=1)
            
            if compare > datetime_:
                print("-----")
                all_info.remove(item)
        
        
        if all_info[-1]["y"] > -10:
            all_info[0]['info_status'] = "Работает"
            all_info[0]['color'] = "#3CB371"
        elif all_info[-1]["y"] <= -20:
            all_info[0]['info_status'] = "Серьёзный сбой"
            all_info[0]['color'] = "#F08080"
        elif all_info[-1]["y"] <= -15:
            all_info[0]['info_status'] = "Есть проблемы"
            all_info[0]['color'] = "#f5c71a"
            
        print(all_info)

        

        
            
        full_array.append(all_info)

    print("\n",full_array)

    return render(
        request, "index.html",
        {
            "title": "Главная страница",
            
            "full_array": full_array,
            "len": len(full_array),
            "count": count_services(),
        },
    )

    
#рендер страницы с регистрацией нового пользователя
def signup(request):
    return render(request, "registration/signup.html", {"count":  count_services()})

#добавление нового пользователя
def create_user(request):
    # Получаем данные из формы
    username = request.POST.get("username", "Undefined")
    email = request.POST.get("email", "Undefined")
    password = request.POST.get("password", "Undefined")

    # Создаем пользователя и сохраните его в базе данных, делаем его не активированным и входим
    user = User.objects._create_user(username, email, password)
    user.is_confirmed = False
    user.save()
    
    #Входим
    user2 = authenticate(request, username=username, password=password)
    print(user2)
    if user2 is not None:
        login(request, user2)
        print("succsess")
        
    # Создаем письмо 
    mail_subject = 'Активируйте свой аккаунт.'
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = "http://{0}/activate/{1}/{2}".format(current_site, uid, token)
    message = "Привет {0}, активируй свой аккаунт по ссылке\n{1}".format(user.username, activation_link)
    to_email = email
    
    #Отправляем письмо
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

    response = render(request, 'registration/activation.html', {"activate": True, "count":  count_services()})
    
    #Ставим куки с именем пользователя
    if user2 is not None:
        response.set_cookie('username', username)
    return response


#рендер страницы с входом
def log_in(request):
    return render(request, "registration/login.html", {"count":  count_services()})

#обработка и вход пользователя в аккаунт
def auth(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    error = ""
    if user is not None:
        login(request, user)
        print("passed")
        response = redirect('/')
        response.set_cookie('username', username)
    else:
        error = "Неправильные имя пользователя или пароль"
        
        #если неправильные имя пользователя или пароль, то рендерим тоже страницу с входом и кидаем в перемнную error сообщение об ошибки
        response = render(request, "registration/login.html", {"error": error, "count":  count_services()})
    return response

#выход из аккаунта
def log_out(request):
    logout(request)
    response = redirect("/")
    response.delete_cookie('username')
    return response

#активация аккаунта 
def activate(request, uid, token):
    #пробуем расшифровать зашифрованное id пользователя и пробуем найти его в БД
    try:
        uid = force_str(urlsafe_base64_decode(uid).decode())
       
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): #если выдает ошибки, то пишем, что нет такого пользователя
        user = None
    if user is not None and account_activation_token.check_token(user, token): #если пользователь есть и токен совпадает, ставим ему активацию и входим в акк
        user.is_confirmed = True
        user.save()
        login(request, user)

        #и передаем флажок успешной активации True
        return render(request, 'registration/activation.html', {"successful_activation": True, "count":  count_services()})
                
    else: #если токен или пользователь не тот, то ставим флажок False
        return render(request, 'registration/activation.html', {"successful_activation": False, "count":  count_services()})

#рендер админской панели
def admin_panel(request, **kwargs):
    
    reports = Report.objects.exclude(message="").exclude(is_moderated=True).values("id","types", "service_slug", "message", "users_name")
  
    reports = list(reports)

    for report in reports:
        slug = report['service_slug']
        service = Service.objects.get(slug=slug)
        url = service.url
        report['service_slug'] = url
        report['service_name'] = service.name
    print(reports)


    user = request.user
    #если пользователь не админ, то его не пускает
    if user.is_staff == True:
        return render(request, 'admin_panel.html', {"reports": reports, "count": count_services(),})
        
    else:
        return redirect("/")

#функция одобрения репорта
def moderate_report(request, id):
    if request.user.is_staff:
        report = Report.objects.get(id=id)
        report.is_moderated = True
        report.save()

    return redirect(admin_panel)

#удаление репорта если он не прошел модерацию
def cancel_report (request, id):
    if request.user.is_staff:
        report = Report.objects.get(id=id)
        report.delete()

    return redirect(admin_panel)


def add_report(request, slug):
    #получаем данные из формы
    try:
        types = request.POST["type"]
    except MultiValueDictKeyError:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    message = request.POST["message"]
    #если тип проблемы не указан, то редиректим назад
    if types == " ":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #получаем никнейм пользователя
    user = request.user
    #добавляем в таблицу репортов инфу о новом репорте
    if message == "":
        Report.objects.update_or_create(types=str(types), message=message, users_name=user, service_slug=slug, is_moderated=True, time=str(datetime.now().replace(microsecond=0)))
    else:
        Report.objects.update_or_create(types=str(types), message=message, users_name=user, service_slug=slug, is_moderated=False, time=str(datetime.now().replace(microsecond=0)))

    #дальше добавлем айдишник нового репорта в таблицу сервиса
    
    service = Service.objects.get(slug=slug)
    last_id = Report.objects.latest("id")
    last_id = last_id.id
    reports = service.reports
    reports = reports + ", "+ str(last_id)
    Service.objects.filter(slug=slug).update(reports=reports)

    #редиректим на предыдущию страницу, когда все сделали
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#добавляет сервис в БД
def add_service(request):
    #поулчает данные из формы
    name = request.POST["name"]
    
    url = request.POST["url"]
    
    abbriviation = request.POST["abbriviation"]
    #просто дформатирует ссылку
    
    #ставит слаг(идентификатор), транслитерируем его и делаем нижнего регистра
    # to_slug = "".join(word[0] for word in name.upper().split())
    # slug = translit(to_slug, "ru", reversed=True).lower()
    slug = re.sub(r'https://', '', url)
    slug = re.sub(r'www.', '', slug)
    slug = re.sub(r'.ru/', '', slug)
    slug = re.sub(r'.ru', '', slug)
    #получаем картинку из формы
    handle_uploaded_file(request.FILES['img'], slug)
    #создаем путь для картинки с названием от слага
    image = "/media/services_images/" + slug + ".png"
    #добавляеет в БД данные
    Service.objects.update_or_create(name=name, url=url, slug=slug, abbreviation=abbriviation, image=image, status='200,', reports='|', time=f'{str(datetime.now().replace(microsecond=0))},')
    return redirect(admin_panel)


#рендер страницы любого сервиса по переданному слагу
def show_service(request, service_slug, **kwargs):
    service = get_object_or_404(Service, slug=service_slug)#ищет сервис в БД по слагу, если не находит возвращает 404 код
    content = model_to_dict(service)#переводит данные найденного сервиса в словрь

        
    all_info = []

    time = (service.time).split(",")
    time = [i[:].strip() for i in time]
    del time[-1]

    for t in time:
        datetime_dict = {}
        time_ = t[11:]
        date = t[:-9]
        datetime_dict['year'] = int(date[:-6])
        datetime_dict['month'] = int(date[5:-3])
        datetime_dict['day'] = int(date[8:])
        datetime_dict['hour'] = int(time_[:-6])
        datetime_dict['minute'] = int(time_[3:-3])
        datetime_dict['second'] = int(time_[6:])
            
        all_info.append(datetime_dict)
       
     
   

    
    
    status = (service.status).split(",")
    del status[-1]
        
    status = [int(i.strip()) for i in status]

    for s in range(len(status)):
        if status[s] >= 200 and status[s] < 300:
                status[s] = 1
        elif status[s] >= 500 and status[s] < 600:
                status[s] = 20
        elif status[s] >= 400 and status[s] < 500:
                status[s] = 15
        elif status[s] >= 300 and status[s] < 400:
                status[s] = 5
        elif status[s] >= 100 and status[s] < 200:
                status[s] = 10

    reports = (service.reports).split("|")
        
    
    count_rep = []
    for report in reports:
        report = report.split(",")
        reports_count = len(report)
        count_rep.append(reports_count)
        

    incedents = [a*b*(-1) for a,b in zip(count_rep,status)]
    

    for dt, i in zip(all_info, incedents):
        dt['y'] = i
        
        
    for inf in all_info:
        inf['name'] = service.name
        inf['slug'] = service.slug

    try:
        please_login = kwargs['please_login']
        content['please_login'] = please_login
    except KeyError:
        pass

    try:
        please_confirm = kwargs['please_confirm']
        content['please_confirm'] = please_confirm
    except KeyError:
        pass

    try:
        username = request.user
        user = get_object_or_404(User, username=username)
        subscribes = user.subscribes
        if service_slug in subscribes:
            subscribe_exist = 1
            content['subscribe_exist'] = subscribe_exist
            
    except:
        pass

    content = content | {"all_info":all_info}
    
    
    raiting = Raiting.objects.filter(service_name=service_slug)
    rates = []
    
    score = 0
    for rate in raiting:
        rate = model_to_dict(rate)
        rate['user_raiting_bucket'] = [0]*rate['rate']
        rates.append(rate)
        score += rate['rate']
        # delta = time_dif(f"{raiting[-1]['year']}-{raiting[-1]['month']}-{raiting[-1]['day']} {raiting[-1]['hour']}:{raiting[-1]['minute']}:{raiting[-1]['second']}")
        # rate['delta'] = delta 
        
    feedbacks_counts = len(raiting)
    if len(raiting) == 0:
        feedbacks_counts = 1
    score = round((score/feedbacks_counts), 2)
    
    rates = list(func_chunk(rates[::-1], 4))
  

    # print(list(func_chunk(rates[::-1], 4)))

    content = content|{"feedbacks": rates}
    content['score'] = score
    content['report_pages'] = len(rates)
    content['feedback_number'] = len(raiting)
    content['buckets'] = [0] * int(str(score)[:1])
    
    
    if all_info[-1]["y"] > -10:
        content['info_status'] = "Работает"
        content['color'] = "#3CB371"
    elif all_info[-1]["y"] <= -20:
        content['info_status'] = "Серьёзный сбой"
        content['color'] = "#F08080"
    elif all_info[-1]["y"] <= -15:
        content['info_status'] = "Есть проблемы"
        content['color'] = "#f5c71a"
    
    #удаляются занчения, сделаные не за полседние 24 часа   
    for item in list(all_info):
            
            
            datetime_ = datetime.strptime(f"{item['year']}-{item['month']}-{item['day']} {item['hour']}:{item['minute']}:{item['second']}", "%Y-%m-%d %H:%M:%S")
            
            compare = datetime.now().replace(microsecond=0)
            compare -= timedelta(days=1)
    
            
            if compare > datetime_:
                print("-----")
                all_info.remove(item)  
    print(content)

    delta = time_dif(f"{all_info[-1]['year']}-{all_info[-1]['month']}-{all_info[-1]['day']} {all_info[-1]['hour']}:{all_info[-1]['minute']}:{all_info[-1]['second']}")
    content['delta'] = delta
    
    content["count"] =  count_services()

    return render(request, 'service.html', content)#рендерит шаблон и передает ему словарь




def add_subscribe(request, slug):
    username = request.user
    
    try:
        user = User.objects.get(username=username)

        if not user.is_confirmed:
             please_confirm = 1
             return show_service(request, slug, **{"please_confirm": please_confirm})
        print(username)
        subscribes = user.subscribes
        
        if subscribes == None:
            subscribes = ""
        if slug in subscribes:
            return redirect(f'service/{slug}')
           
        subscribes = subscribes + " " + str(slug) + ","
        user.subscribes = subscribes
        user.save()
    except ObjectDoesNotExist:
        please_login = 1
        return show_service(request, slug, **{"please_login": please_login})

    return redirect(f'service/{slug}')

def delete_subscribe(request, slug):
     username = request.user
    
     try:
        user = User.objects.get(username=username)
        print(username)
        subscribes = user.subscribes
        
        if subscribes == None:
            subscribes = ""
            return redirect(f'service/{slug}')
        
        subscribes = subscribes.split(slug+",")
        subscribes = str(subscribes[0]+subscribes[1])
        user.subscribes = subscribes
        user.save()
        user.save()
     except ObjectDoesNotExist:
        please_login = 1
        return show_service(request, slug, **{"please_login": please_login})

     return redirect(f'service/{slug}')


def search(request, **kwargs):

    try:#пробуем достать из формы запрос
       query = request.POST["search"]
    except: #если не получается, ищем в дополнительных аргументах kwargs
        if 'query' in kwargs:
            query = kwargs['query'] #если сеть запрос в доп аргумнентах, то берем его
            
        else:
            query = "" #если нет в аргументах, то делаем запрос пустым (он выведет все записи тогда)
            
    query = urllib.parse.unquote(query) #и обрабатываем, если он url encoded 
    #фильтруем строку регулярками на наличие плохих символов
    query = re.sub('[\^<>%$#\'/]', '', query)
    
    print(query)
    #делаем запросы к БД через регулярки
    queryset = Service.objects.filter(Q(name__iregex=rf"{query}") | Q(url__iregex=rf"{query}") | Q(abbreviation__iregex=rf"{query}"))
    print(queryset[0])
    
    return render(request, "search.html", {"queryset":queryset, "search_query": query, "count":  count_services()})



def tg_activate(request, tgid):
    username = request.user
    tgid = str(base64.b64decode(tgid).decode('utf-8'))
    try:
        user = User.objects.get(username=username)

        if not user.is_confirmed:
            return account(request, **{'please_confirm': True})
        

       
        user_tgid = user.tgid
        print(user_tgid, tgid)
        if user_tgid == None:
            user_tgid = ""
            
        if tgid == user_tgid:
            return  account(request, **{'already_exist': True})

        user.tgid = tgid
        user.save()
        return account(request, **{'tg': True})

    except ObjectDoesNotExist:
        return log_in(request)

    
def add_feedback(request, slug):
    
    username = request.user
    message = request.POST["feedback_message"]
    value = request.POST["feedback"]
    print(message, value)
    
    try:
        raiting = Raiting.objects.get(users_name=username)
        if message != "":
            Raiting.objects.create(users_name=username, rate=value, message=message, service_name=slug)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        
        raiting = Raiting.objects.create(users_name=username, rate=value, message=message, service_name=slug)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def account(request, **kwargs):
    username = request.user
    
    print(kwargs)
    try:
        user = User.objects.get(username=username)

        if user.subscribes:
            subscribes = user.subscribes.split(',')
            subscribes = [i[:].strip() for i in subscribes]
            del subscribes[-1]
        

            print(subscribes)
            
            c_s = []
            for service in subscribes:
                
                if Service.objects.get(slug=service):
                    s = Service.objects.get(slug=service)
                    subs = {}
                    
                    subs['abb'] = s.abbreviation
                    subs['slug'] = s.slug

                    c_s.append(subs)
                else:
                    c_s.append("Нет подписок")
                
            print(c_s)

        else:
            c_s = ""

        dc = model_to_dict(user)

        try:
            please_confirm = kwargs['please_confirm']
            dc['please_confirm'] = please_confirm            
        except:
            pass

        try:
            already_exist = kwargs['already_exist']
            dc['already_exist'] = already_exist
        except:
            pass
       
        try:
            tg = kwargs['tg']
            dc['tg'] = tg
        except:
            pass
        
            print(dc)
        return render(request, "account.html", {"dict": dc, "subs": c_s, "count":  count_services()})
    except ObjectDoesNotExist:
        return log_in(request)

def addmin(request):
    username = request.POST["u"]
    cuser = request.user
    cu = User.objects.get(username=cuser)

    if cu.is_staff:
        use = User.objects.get(username=username)
        use.is_staff = 1
        use.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def addmindel(request):
    username = request.POST["d"]
    cuser = request.user
    cu = User.objects.get(username=cuser)

    if cu.is_staff:
        use = User.objects.get(username=username)
        use.is_staff = 0
        use.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
