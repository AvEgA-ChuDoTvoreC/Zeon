# Zeon

Flask-проект для коммуникации датчиков с Zabbix. Swagger документация на API имеется.

Иерархия папок проекта подразумевает сборку в DEB-пакет и запуск его под web-сервером Apache2, 
а также регистрацию в Consul. Конфиги в соответствующих местах, согласно Debian File System.

## Инструкция для запуска приложения

### Создание и активация виртуального окружения (опционально)

```bash
$ python3 -m venv <название виртуального окружения>
$ source <название виртуального окружения>/bin/activate
```

### Установка зависимостей для проекта
```bash
$ pip install -r requirements.txt
```

### Запусти приложение
```bash
python run.py
```

### Swagger документация проекта
В адресной строке браузера перейди по следующему URL
```
http://127.0.0.1:5000/apidocs
```

### Конфигурирование приложения
Для этого установи соответствующее значение 
для переменной DEBUG в файле .env (по умолчанию True, если не задана переменная)
* debug - для отладки
* prod - для прода

### Настройка пространства
Установи переменную окружения для Flask
```bash
$ export FLASK_APP=run.py
```

Создай базу
```bash
docker run --name my-postgresql \
           -e POSTGRES_USER=neo \
           -e POSTGRES_PASSWORD=123qweasd \
           -e POSTGRES_DB = zeon \
           -p 5432:5432 \
           -v /data:/var/lib/postgresql/data \
           -d postgres
docker_cont_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-postgresql)
psql -U postgres -h ${docker_cont_ip} -p 5432
```

Запусти Zabbix
```bash
docker network create --subnet 172.20.0.0/16 \
                      --ip-range 172.20.240.0/20 \
                      zabbix-net
docker run --name postgres-server \
           -t \
           -e POSTGRES_USER="zabbix" \
           -e POSTGRES_PASSWORD="zabbix_pwd" \
           -e POSTGRES_DB="zabbix" \
           --network=zabbix-net \
           --restart unless-stopped \
           -d \
           postgres:latest
docker run --name zabbix-server-pgsql \
           -t \
           -e DB_SERVER_HOST="postgres-server" \
           -e POSTGRES_USER="zabbix" \
           -e POSTGRES_PASSWORD="zabbix_pwd" \
           -e POSTGRES_DB="zabbix" \
           --network=zabbix-net \
           -p 10051:10051 \
           --restart unless-stopped \
           -d \
           zabbix/zabbix-server-pgsql:ubuntu-4.0-latest
docker run --name zabbix-web-nginx-pgsql \
           -t \
           -e ZBX_SERVER_HOST="zabbix-server-pgsql" \
           -e DB_SERVER_HOST="postgres-server" \
           -e POSTGRES_USER="zabbix" \
           -e POSTGRES_PASSWORD="zabbix_pwd" \
           -e POSTGRES_DB="zabbix" \
           --network=zabbix-net \
           -p 443:8443 \
           -p 80:8080 \
           -v /etc/ssl/nginx:/etc/ssl/nginx:ro \
           --restart unless-stopped \
           -d \
           zabbix/zabbix-web-nginx-pgsql:ubuntu-4.0-latest
```

Сделай миграции
```bash
$ flask init
$ flask db migrate -m <комментарий>
```

Примени миграции для БД
```bash
$ flask db upgrade
$ flask db downgrade
```

Управляй Flask через консоль. ```url_map``` - для отображения API маршрутов
```bash
$ flask shell
  >>> app.url_map 
```
```python
from apps.api import models

models.db.session.add(
    models.Users(
        username='Pedor', 
        email='pedor@email.ru', 
        password='hernur'
    ))

models.db.session.commit()
```

### Что если у тебя python3.5 ?

Установи Python3.5
```bash
$ sudo apt-get install build-essential checkinstall
$ sudo apt-get install libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdm-dev libc6-dev libbz2-dev
$ sudo apt-get install libssl-dev openssl
$ wget https://www.python.org/ftp/python/3.5.3/Python-3.5.3.tgz
$ tar -xzvf Python-3.5.3.tgz
$ cd Python-3.5.3
$ sudo ./configure --enable-optimizations
$ make
$ sudo make altinstall
```

Настрой свое окружение
```bash
$ python3.5 -m venv ./venv --without-pip
$ curl https://bootstrap.pypa.io/pip/3.5/get-pip.py -o get-pip.py
$ python get-pip.py
$ python -m pip install <packages>
  # Если баг с pip:
$ export FLASK_APP=./run.py
$ python -m flask run
$ python -m pip freeze > requirements.txt
$ python -m flask db init
```

Requirement:
```bash
$ pip install setuptools==40.9.0
```

```dotenv

```