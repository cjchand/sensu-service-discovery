FROM cjchand/sensu-client:http

RUN yum -y --setopt=tsflags=nodocs install httpd php php-mysql python-pip && \
    yum clean all

RUN pip install requests jinja2

COPY httpd.conf /etc/supervisord.d/httpd.conf

# Commenting this out, as we want to apply it dyamically via Sens subscription membership
# COPY check-http.json /etc/sensu/conf.d/check-http.json

COPY index.html /var/www/html/index.html
COPY info.php /var/www/html/info.php
COPY ./etc/ /etc/
RUN chown -R sensu:sensu /etc/sensu
COPY client.json.j2 /tmp/client.json.j2

EXPOSE 80