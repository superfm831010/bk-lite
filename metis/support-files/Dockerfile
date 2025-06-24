FROM python:3.12

WORKDIR /app

ADD . .

RUN pip install -r ./requirements/requirements.in
RUN pip install -r ./requirements/requirements-dev.in

ADD ./support-files/service.conf /etc/supervisor/conf.d/service.conf

#RUN sanic server:bootstrap exec download_models
ENTRYPOINT ["/bin/bash","/app/support-files/startup.sh"]