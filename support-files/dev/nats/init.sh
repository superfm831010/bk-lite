nats -s nats://127.0.0.1:4222 --user admin --password nats_password \
    stream add metrics --subjects="metrics.*" --storage=file \
    --replicas=1 --retention=limits --discard=old \
    --max-age=20m --max-bytes=104857600 --max-consumers=-1 \
    --max-msg-size=-1 --max-msgs=-1 --max-msgs-per-subject=1000000 \
    --dupe-window=5m --no-allow-rollup --no-deny-delete --no-deny-purge