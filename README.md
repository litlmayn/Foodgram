![Yamdb Workflow Status](https://github.com/litlmayn/foodgram-project-react/actions/workflows/main.yml/badge.svg?branch=master&event=push)
### Проект Foodgram - это проект, направленный на поиск новых рецептов!

```
Ссылка на развернутый проект: http://158.160.10.107
```
```
С помощью данной плотформы люди могут делиться рецептами, подписываться на авторов, сохранять любимые рецепты,
а так же скачивать список для покупок.
```

### Мы использовали данный стек технологий для проектирования проекта:
```
Django
DRF
Python
PostgreSQL
Docker
Docker-compose
Gunicorn
Nginx
React
```


### Как запустить проект режиме:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:litlmayn/foodgram-project-react.git
```

```
cd infra
```

Запустить docker-compose:

```
docker-compose up -d --build
```

Выполните по очереди команды:

```
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
sudo docker-compose exec web python manage.py importcsv
```

### Пример env-файла:

```
SECRET_KEY = 'key'
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=user # логин для подключения к базе данных
POSTGRES_PASSWORD=Porol1234 # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
