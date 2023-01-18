from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import  authenticate, logout
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse
from user_model.models import User as u #херня эта VSкодовская выдает ошибку, хотя все работает и со строкой все норм (не обращать внимания)
from .scripts.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


User = get_user_model()

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
    username = request.POST.get("username", "Undefined")
    email = request.POST.get("email", "Undefined")
    password = request.POST.get("password", "Undefined")

    # Создайте пользователя и сохраните его в базе данных, делаем его не активированным и входим
    user = u.objects._create_user(username, email, password)
    user.is_active = False
    
    user.save()
    user2 = authenticate(request, username=username, email=email, password=password)
    print(user2)
    if user2 is not None:
        login(request, user2,  backend='django.contrib.auth.backends.ModelBackend')

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
    # redirect("/").set_cookie('username', username)

    return HttpResponse('Подтвердите свою почту, для завершения регистрации')



#рендер страницы с входом
def log_in(request):
    return render(request, "registration/login.html")

#обработка и вход пользователя в аккаунт
def auth(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        response = redirect('/')
        response.set_cookie('username', username)
    else:
        response = redirect('/login')
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
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse("Вы подтвердили аккаунт, поздравляю")
        # return render(request, 'activation.html')
                
    else: #если токен или пользователь не тот, то пишем, что неправильная ссылка
        return HttpResponse('Неправильная ссылка для активации аккаунта')