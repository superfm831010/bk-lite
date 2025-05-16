import os

NATS_SERVERS = os.getenv("NATS_SERVERS", "")
NATS_NAMESPACE = os.getenv("NATS_NAMESPACE", "bk_lite")
NATS_JETSTREAM_ENABLED = False
