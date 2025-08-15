FROM bklite/metis:base

ENV DEFAULT_DATABASE=neo4j 

WORKDIR /app

ADD . .

ADD ./support-files/service.conf /etc/supervisor/conf.d/service.conf

ENTRYPOINT ["/bin/bash","/app/support-files/startup.sh"]