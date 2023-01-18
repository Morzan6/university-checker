from django.contrib import admin
from django.urls import path, include

from predprof.core import views as core_views

urlpatterns = [
    path("", core_views.index, name="index"),
    #path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("test/", core_views.test),
    path("signup/", core_views.signup), #рендер страницы регистрации
    path("login/", core_views.log_in), #рендер страницы входа
    path("logout/", core_views.log_out), #выход из аккаунта 
    path("auth/", core_views.auth, name="auth"), #вход пользователя (обработка)
    path("create_user/", core_views.create_user, name="create_user"), #создание и добавление нового пользователя в бд 
    path('activate/<str:uid>/<str:token>', core_views.activate, name='activate'), #проверка пользователя и активация аккаунта
    
]
