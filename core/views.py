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
from transliterate import translit
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

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

#рендер админскйо панели
def admin_panel(request, **kwargs):
    
    user = request.user
    #если пользователь не админ, то его не пускает
    if user.is_staff == True:
        return render(request, 'admin_panel.html',)
        
    else:
        return redirect("/")

#добавляет сервис в БД
def add_service(request):
    #поулчает данные из формы
    name = request.POST["name"]
    url = request.POST["url"]
    
    # image = request.FILES.get["img"]
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


