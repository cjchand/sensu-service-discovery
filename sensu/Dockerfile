FROM hiroakis/docker-sensu-server

# Had to add the rpm --rebuilddb for some reason. Hope it's just a temp issue and I can remove it later

RUN rpm --rebuilddb &&  \
    yum -y --setopt=tsflags=nodocs install python-pip && \
    yum clean all

RUN pip install requests argparse

COPY ./etc/ /etc/

RUN wget https://repositories.sensuapp.org/yum/6/x86_64/sensu-1.0.0-1.el6.x86_64.rpm && rpm -Uhv sensu-1.0.0-1.el6.x86_64.rpm
