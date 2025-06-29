FROM python:3.10
WORKDIR /apps

RUN apt-get update -y
RUN apt-get install -y vim supervisor

ADD ./support-files/release/supervisor/app.conf  /etc/supervisor/conf.d/app.conf
ADD ./support-files/release/supervisor/nats.conf  /etc/supervisor/conf.d/nats.conf
ADD ./support-files/release/supervisor/beat.conf  /etc/supervisor/conf.d/beat.conf
ADD ./support-files/release/supervisor/celery.conf  /etc/supervisor/conf.d/celery.conf
ADD ./support-files/release/supervisor/consumer.conf  /etc/supervisor/conf.d/consumer.conf

ADD . .

RUN pip install -r ./requirements/requirements-core.txt
RUN pip install -r ./requirements/requirements-system_mgmt.txt
RUN pip install -r ./requirements/requirements-cmdb.txt
RUN pip install -r ./requirements/requirements-console.txt
RUN pip install -r ./requirements/requirements-monitor.txt
RUN pip install -r ./requirements/requirements-node_mgmt.txt
RUN pip install -r ./requirements/requirements-opspilot.txt
RUN pip install -r ./requirements/requirements-mlops.txt

RUN chmod +x ./support-files/release/startup.sh
ENTRYPOINT ["/bin/bash","/apps/support-files/release/startup.sh"]