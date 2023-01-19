FROM ubuntu/apache2:2.4-22.04_beta
RUN apt-get update -y \
    && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 

# RUN apt-get install libapache2-mod-wsgi-py3
COPY ./django-site-config.conf etc/apache2/sites-available
RUN a2ensite django-site-config.conf \
  && a2enmod proxy \
  && a2enmod proxy_http \
  && a2enmod wsgi
