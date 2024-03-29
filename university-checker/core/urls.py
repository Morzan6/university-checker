# from django.contrib import admin
from django.urls import path, include
from config import settings
from core import views as core_views
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.urls import path, re_path

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path("", core_views.index, name="index"),
    path("service/university-checker/", core_views.redirect_main),
    path("__reload__/", include("django_browser_reload.urls")),
    path("signup/", core_views.signup), #рендер страницы регистрации
    path("login/", core_views.log_in), #рендер страницы входа
    path("logout/", core_views.log_out), #выход из аккаунта 
    path("auth/", core_views.auth, name="auth"), #вход пользователя (обработка)
    path("create_user/", core_views.create_user, name="create_user"), #создание и добавление нового пользователя в бд 
    path('activate/<str:uid>/<str:token>', core_views.activate, name='activate'), #проверка пользователя и активация аккаунта  
    path("add_service/", core_views.add_service, name="add_service"),#добавляет сервис в БД
    path("admin_panel/", core_views.admin_panel),#рендерит админ панель
    path('service/<slug:service_slug>/', core_views.show_service, name='service'), #рендерит страницу любого сервиса по переданному слагу
    path('add_report&<slug:slug>/', core_views.add_report, name="add_report"), #добавление репорта
    path('moderate_report&<int:id>', core_views.moderate_report, name="moderate_report"), #одобрение репорта
    path('cancel_report&<int:id>', core_views.cancel_report, name="cancel_report"), #отмена репорта
    path('search/<str:query>', core_views.search, name="search_from_url"), #поиск по url
    path('search/', core_views.search, name="search"), #поиск по форме
    path('add_subscribe&<slug:slug>', core_views.add_subscribe, name="add subscribe"),
    path('delete_subscribe&<slug:slug>', core_views.delete_subscribe, name="add subscribe"),
    path('activatetg&<str:tgid>/', core_views.tg_activate),
    path('add_feedback&<slug:slug>/', core_views.add_feedback),
    path('account/', core_views.account),
    path('addmin/', core_views.addmin),
    path('addmindel/', core_views.addmindel),
    re_path(r'^favicon\.ico$', favicon_view),
]

#Дебаг медиа файлов 
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)