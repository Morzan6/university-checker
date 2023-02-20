Установить docker, docker-compose, nginx

```
sudo apt update
sudo apt upgrade
sudo apt install docker
sudo apt install docker-compose
sudo apt install nginx
docker pull nginx
docker pull python:3.9
docker-compose build
docker-compose up &
```

Обновляем apt

$ sudo apt update

$ sudo apt upgrade


Загружаем репозиторий с GitHub, переходим в его папку, по умолчанию папка – university-checker-master/

$ git clone https://github.com/Morzan6/university-checker-master.git

$ cd university-checker-master

Выполняем команды с установкой всех необходимых утилит:


$ sudo apt install python3 apt-transport-https  ca-certificates  curl  gnupg  lsb-release nano

$ curl -fsSL https://get.docker.com -o get-docker.sh

$ sudo sh get-docker.sh

$ sudo usermod -aG docker $USER

$ sudo apt install docker-compose

$ sudo apt install nginx

Меняем в файле ./nginx/mysite_nginx.conf значение server_name в строчке 11 на собственный домен или IP адрес 

$ nano ./nginx/mysite_nginx.conf

11    server_name     localhost; # замените на собственный домен или IP адрес

 
Добавляем наш домен или IP адрес в разрешенные хосты в файле . /university-checker/config/settings.py

$ nano . /university-checker/config/settings.py


28    ALLOWED_HOSTS = ['university-checker.ru', 'localhost', ‘ваш домен или IP’]

Устанавливаем в Docker необходимые утилиты

$ docker pull nginx

$ docker pull python:3.9


Запускаем сборку проекта

$ docker-compose build

Запускаем работу проекта и переводим выполнение на фон

$ docker-compose up &
