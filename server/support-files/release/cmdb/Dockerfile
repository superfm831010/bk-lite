FROM python:3.10
WORKDIR /apps

RUN apt-get update -y
RUN apt-get install -y vim supervisor

ADD ./support-files/release/cmdb/supervisor/app.conf  /etc/supervisor/conf.d/app.conf
ADD ./support-files/release/cmdb/supervisor/beat.conf  /etc/supervisor/conf.d/beat.conf
ADD ./support-files/release/cmdb/supervisor/celery.conf  /etc/supervisor/conf.d/celery.conf

ADD . .

RUN find ./apps/ -mindepth 1 -maxdepth 1 -type d \( ! -name base -a ! -name core -a ! -name rpc -a ! -name "cmdb" \) -print0 | xargs -0 rm -rf

RUN pip install -r ./requirements/requirements-core.txt
RUN pip install -r ./requirements/requirements-cmdb.txt

RUN chmod +x ./support-files/release/cmdb/startup.sh
ENTRYPOINT ["/bin/bash","/apps/support-files/release/cmdb/startup.sh"]