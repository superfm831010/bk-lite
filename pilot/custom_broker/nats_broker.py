import asyncio
import json
from typing import Optional, Text, Dict, Any

import nats
from loguru import logger
from rasa.core.brokers.broker import EventBroker
from rasa.shared.utils.io import DEFAULT_ENCODING

from core.server_settings import server_settings


class NatsEventBroker(EventBroker):
    """NATS event broker for publishing Rasa events."""

    def __init__(
        self,
        url: Text = "nats://localhost:4222",
        subject: Text = "rasa.events",
        **kwargs: Any,
    ):
        """Initialize NATS event broker.

        Args:
            url: NATS server URL
            subject: NATS subject to publish events to
            **kwargs: Additional keyword arguments
        """
        self.url = url
        self.subject = subject
        self._nc: Optional[nats.NATS] = None
        self._loop = None

    @classmethod
    def from_endpoint_config(
        cls, broker_config: Dict[Text, Any]
    ) -> "NatsEventBroker":
        """Create NatsEventBroker from endpoint configuration.

        Args:
            broker_config: Broker configuration dictionary

        Returns:
            NatsEventBroker instance
        """
        return cls(
            url=broker_config.get("url", "nats://localhost:4222"),
            subject=broker_config.get("subject", "rasa.events"),
            **{k: v for k, v in broker_config.items()
               if k not in ["url", "subject", "type"]}
        )

    async def _connect(self) -> None:
        """Connect to NATS server."""
        if self._nc is None or not self._nc.is_connected:
            try:
                self._nc = await nats.connect(self.url)
                logger.info(f"Connected to NATS server at {self.url}")
            except Exception as e:
                logger.error(f"Failed to connect to NATS server: {e}")
                raise

    def _ensure_connection(self) -> None:
        """Ensure connection to NATS server exists."""
        if self._loop is None:
            try:
                self._loop = asyncio.get_event_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)

        if self._nc is None or not self._nc.is_connected:
            if self._loop.is_running():
                # If loop is already running, schedule the connection
                task = asyncio.create_task(self._connect())
                # Wait for the connection to complete
                while not task.done():
                    pass
            else:
                self._loop.run_until_complete(self._connect())

    def publish(self, event: Dict[Text, Any], headers: Optional[Dict] = None) -> None:
        """Publish event to NATS.

        Args:
            event: Event dictionary to publish
            headers: Optional headers (not used in NATS)
        """
        try:
            # Add bot_id to event
            event["bot_id"] = server_settings.munchkin_bot_id

            # Ensure connection
            self._ensure_connection()

            # Serialize event to JSON
            message = json.dumps(
                event, ensure_ascii=False).encode(DEFAULT_ENCODING)

            # Publish to NATS
            if self._loop.is_running():
                asyncio.create_task(self._nc.publish(self.subject, message))
            else:
                self._loop.run_until_complete(
                    self._nc.publish(self.subject, message))

            logger.info(
                f"NatsEventBroker published event to subject '{self.subject}': {event}")

        except Exception as e:
            logger.error(f"Failed to publish event to NATS: {e}")
            raise

    def is_ready(self) -> bool:
        """Check if the broker is ready to publish events.

        Returns:
            True if broker is ready, False otherwise
        """
        try:
            self._ensure_connection()
            return self._nc is not None and self._nc.is_connected
        except Exception as e:
            logger.error(f"Error checking NATS broker readiness: {e}")
            return False

    def close(self) -> None:
        """Close connection to NATS server."""
        if self._nc and self._nc.is_connected:
            try:
                if self._loop and not self._loop.is_closed():
                    if self._loop.is_running():
                        asyncio.create_task(self._nc.close())
                    else:
                        self._loop.run_until_complete(self._nc.close())
                logger.info("Closed connection to NATS server")
            except Exception as e:
                logger.error(f"Error closing NATS connection: {e}")
            finally:
                self._nc = None
