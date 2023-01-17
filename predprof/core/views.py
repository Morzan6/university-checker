from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import  authenticate, logout
from django.contrib.auth import login
from django.http import HttpResponse

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

    # Создайте пользователя и сохраните его в базе данных и войти
    user = User.objects.create_user(username, email, password)
    user = authenticate(request, username=username, password=password)
    login(request, user)
    response = redirect('/')
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