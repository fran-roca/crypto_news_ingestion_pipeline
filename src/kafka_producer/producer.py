import sys
if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaProducer
import json
import logging
from src.config.settings import get_settings

settings = get_settings()


class KafkaProducerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        return cls._instance

    def send_message(self, message):
        try:
            future = self.producer.send(settings.KAFKA_TOPIC, value=message)
            self.producer.flush()
            future.get(timeout=10)
            logging.info(f"Message sent successfully: {message['title']}")
        except Exception as e:
            logging.error(f"Error sending message to Kafka: {e}")
            raise
