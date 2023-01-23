# GitHub ♥️ Django

Будем делать тут

```python
python manage.py runserver
```
https://morzan6-organic-doodle-69gx6797jvr24w6x-8000.preview.app.github.dev/ - 

 ```
 20.01.2023 00:52
 * Добавлены сообщения об ошибках при неправильном вводе пароля или имени пользователя на signup и login
 * Закончена функция подтверждения пользователя через почту (пока работает только с yandex почтой)
 * Исправлено отображение index (главной страницы) при разных состояниях аккаунта (подтвержден/неподтвержден)
 * Исправлены баги с входом при создании нового пользователя
 ```
 ```
 21.01.2023 12:20
 * Изменена иерархия папок

*
├── config #папка конфига с настройками 
│   ├── asgi.py
│   ├── settings.py
│   └── wsgi.py
├── core #ядро, основная папка проекта
│   ├── apps.py
│   ├── scripts #папка со скриптами разными
│   ├── static #папка с картинками, css и прочими дополнительными штуками
│   ├── templates #папка с html-шаблонами 
│   ├── urls.py #обработчик url-запросов
│   └── views.py #функции, которые выполняет сайт при переходе на разные url
├── db.sqlite3 #база данных
├── manage.py #файл для работы через терминал и отправки команд
├── README.md #это для гитхаба
├── requirements.txt #необходимые библиотеки для python
└── user_model #папка с моделью пользователя для БД
    ├── apps.py
    ├── migrations #микрации модели в БД
    └── models.py #сама модель

 * Добавлен рендер страницы /activate из html-шаблона, с передачей инфы об успешной или неуспешной активации
 ```
 
 ```
 22.01.2023 16:00
 
 * Добавлены модели (таблицы в БД) для самого сервиса, репортов пользователей и оценок. Все расписано в фигме, что за что отвечает 
 https://www.figma.com/file/ymyXt2sMhfXjmIcDzosDHr/PredProf?node-id=0%3A1&t=9gIgnzuyBXJZ8MVs-0
 
 ```

```
23.01.2021 23:56

*Добавлена тестовая админ-панель с функцией "добавления ресурса для отслеживания его доступности" - форма с именем и url, которая летит в таблицу БД о сервисах
 соответственно обычным пользователям запрещен доступ к админ-панеле, их редиректит на главную страницу
* Исправлены модели в БД
* Добавлены новые настройки VS code в devcontainer

```