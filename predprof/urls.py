"""hello_world URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from predprof.core import views as core_views

urlpatterns = [
    path("", core_views.index, name="index"),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("test/", core_views.test),
    path("signup/", core_views.signup), #рендер страницы регистрации
    path("login/", core_views.log_in), #рендер страницы входа
    path("logout/", core_views.log_out), #выход из аккаунта 
    path("auth/", core_views.auth, name="auth"), #вход пользователя (обработка)
    path("create_user/", core_views.create_user, name="create_user"), #добавление нового пользователя в бд и вход в аккаунт (обработка)
    # path('', include('django.contrib.auth.urls')),
]
