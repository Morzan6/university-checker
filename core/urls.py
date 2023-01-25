# from django.contrib import admin
from django.urls import path, include
from config import settings
from core import views as core_views
from django.conf.urls.static import static

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
    path("add_service/", core_views.add_service, name="add_service"),#добавляет сервис в БД
    path("admin_panel/", core_views.admin_panel),#рендерит админ панель
    path('service/<slug:service_slug>/', core_views.show_service, name='service'), #рендерит страницу любого сервиса по переданному слагу
    path('add_report&<slug:slug>/', core_views.add_report, name="add_report")
]

#Дебаг медиа файлов 
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)