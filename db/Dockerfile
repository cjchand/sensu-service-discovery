FROM cjchand/sensu-client:http

RUN yum install -y --setopt=tsflags=nodocs mariadb mariadb-server python-pip && \
    yum clean all

RUN pip install requests jinja2

# Create data directory for MySQL
VOLUME ["/var/lib/mysql"]

RUN echo "NETWORKING=yes" > /etc/sysconfig/network

# Deploy core MySQL tables 
RUN /usr/bin/mysql_install_db --user=mysql

# Start mysqld to lay down base directory structure
RUN /usr/bin/mysqld_safe --skip-grant-tables &
RUN sleep 10
# Make sure that mysql owns its data directory
RUN chown -R mysql:mysql /var/lib/mysql

COPY mysql.conf /etc/supervisord.d/mysql.conf

RUN sensu-install -P sensu-plugins-mysql
COPY ./etc/ /etc/
RUN chown -R sensu:sensu /etc/sensu
COPY client.json.j2 /tmp/client.json.j2

