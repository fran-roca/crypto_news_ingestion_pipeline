import logging
from src.kafka_producer.producer import KafkaProducerSingleton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_health():
    try:
        # Check Kafka connection
        producer = KafkaProducerSingleton()
        producer.producer.bootstrap_connected()
        logger.info("Health check passed")
        return 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return 503

if __name__ == "__main__":
    check_health()