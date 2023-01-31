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
from services_model.models import Service
from reports_model.models import Report
from transliterate import translit
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.db.models import Q
import re
import urllib.parse

User = get_user_model()

#обработчик главной страницы
def index(request):
    return render(
        request, "index.html",
        {
            "title": "Главная страница",      
        },
    )

def test(request):
    return render(request, "test.html")
    
#рендер страницы с регистрацией нового пользователя
def signup(request):
    return render(request, "registration/signup.html")

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
    message = "Привет {0},\n {1}".format(user.username, activation_link)
    to_email = email
    
    #Отправляем письмо
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

    response = HttpResponse(' Подтвердите свою почту, для завершения регистрации <br/><a class="underline underline-offset-1" href="/">Главная</a>')
    
    #Ставим куки с именем пользователя
    if user2 is not None:
        response.set_cookie('username', username)
    return response


#рендер страницы с входом
def log_in(request):
    return render(request, "registration/login.html")

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
        response = render(request, "registration/login.html", {"error": error})
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
        return render(request, 'registration/activation.html', {"successful_activation": True})
                
    else: #если токен или пользователь не тот, то ставим флажок False
        return render(request, 'registration/activation.html', {"successful_activation": False})

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
        return render(request, 'admin_panel.html', {"reports": reports})
        
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
    types = request.POST["type"]
    message = request.POST["message"]
    #если тип проблемы не указан, то редиректим назад
    if types == " ":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #получаем никнейм пользователя
    user = request.user
    #добавляем в таблицу репортов инфу о новом репорте
    Report.objects.update_or_create(types=str(types), message=message, users_name=user, service_slug=slug)

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
    #просто дформатирует ссылку
    if url[:6] != "https:/" or url[:5] != "http:/":
        url = "https:/" + url
    #ставит слаг(идентификатор), транслитерируем его и делаем нижнего регистра
    slug = translit(name, "ru", reversed=True).lower()
    #получаем картинку из формы
    handle_uploaded_file(request.FILES['img'], slug)
    #создаем путь для картинки с названием от слага
    image = "/media/services_images/" + slug + ".png"
    #добавляеет в БД данные
    Service.objects.update_or_create(name=name, url=url, slug=slug, image=image)
    return redirect(admin_panel)


#рендер страницы любого сервиса по переданному слагу
def show_service(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug)#ищет сервис в БД по слагу, если не находит возвращает 404 код
    content = model_to_dict(service)#переводит данные найденного сервиса в словрь

    return render(request, 'service.html', content)#рендерит шаблон и передает ему словарь


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
    queryset = Service.objects.filter(Q(name__iregex=rf"{query}") | Q(url__iregex=rf"{query}"))
    
    return render(request, "search.html", {"queryset":queryset, "search_query": query})