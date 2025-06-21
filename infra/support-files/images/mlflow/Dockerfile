FROM python:3.12

RUN apt-get update && \
    apt-get install -y supervisor &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD ./mlflow_server.py ./mlflow_server.py
ADD ./mlflow.conf /etc/supervisor/conf.d/mlflow.conf

RUN chmod +x ./mlflow_server.py
ADD ./startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh
ENTRYPOINT [ "bash","/app/startup.sh" ]

