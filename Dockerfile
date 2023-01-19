# FROM ubuntu:20.04
# RUN apt-get update
# RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
# RUN apt-get -y install python3 libapache2-mod-wsgi-py3
# RUN ln /usr/bin/python3 /usr/bin/python
# RUN apt-get -y install python3-pip
# RUN ln /usr/bin/pip3 /usr/bin/pip
# RUN pip install --upgrade pip
# RUN pip install django ptvsd
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /code/
# WORKDIR /code/
# COPY requirements.txt /code
# RUN pip install -r requirements.txt
# COPY . /code/
# ADD ./django-site-config.conf /etc/apache2/sites-available/django-site-config.conf
# RUN a2ensite django-site-config.conf
# RUN service apache2 start
# RUN service apache2 reload
# EXPOSE 80 3500
# CMD ["apache2ctl", "-D", "FOREGROUND"]

FROM python:3.8
RUN pip install --upgrade pip
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends
RUN apt-get install default-mysql-client -y
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

COPY . .
# RUN python manage.py  makemigrations \
#     && python manage.py migrate
# EXPOSE 80
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
 
# ADD ./www/superset_proxy/ /var/www/html/
# RUN apt-get install -y apt-utils vim curl apache2 apache2-utils git
# RUN apt-get -y install python3.6 libapache2-mod-wsgi-py3 
# ADD ./proxy-site-config.conf /etc/apache2/sites-available/000-default.conf 
# RUN chmod 777 /var/www/html/superset_proxy/
# EXPOSE 80
# CMD ["apache2ctl", "-D", "FOREGROUND"]