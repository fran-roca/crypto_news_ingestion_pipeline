import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from src.news_fetcher.news_data_fetcher import NewsDataFetcher
from src.kafka_producer.producer import KafkaProducerSingleton
from src.config.settings import get_settings
from src.config.utils import setup_logging

# Set up logging configurations
setup_logging()


def fetch_and_publish_news():
    logging.info("Starting the news fetching and publishing process.")
    try:
        # Load settings
        settings = get_settings()
        logging.debug("Settings loaded successfully.")

        # Initialize news fetcher
        fetcher = NewsDataFetcher(settings.NEWS_API_KEY)
        logging.info("NewsDataFetcher initialized with API key.")

        # Initialize Kafka producer
        producer = KafkaProducerSingleton()
        logging.info("KafkaProducerSingleton initialized.")

        # Fetch news articles
        articles = fetcher.fetch_all_news()
        logging.info(f"Fetched {len(articles)} articles.")

        # Publish each article to Kafka
        for article in articles:
            message = {
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'publishedAt': article.get('publishedAt')
            }
            try:
                producer.send_message(message)
                logging.debug(f"Message sent to Kafka: {message['title']}")
            except Exception as e:
                logging.error(f"Error sending message to Kafka: {e}")

        logging.info("News fetched and published to Kafka successfully.")
    except Exception as e:
        logging.error(f"Error in news fetcher service: {e}")


def main():
    logging.info("Initializing the news ingestion pipeline.")

    # Initialize and start scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_publish_news, 'interval', minutes=15)
    scheduler.start()
    logging.info("Scheduler started. Job scheduled to run every 15 minutes.")

    try:
        # Keep the program running
        while True:
            time.sleep(60)
            logging.debug("Main loop heartbeat.")
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutting down scheduler.")
        scheduler.shutdown()


if __name__ == "__main__":
    logging.info("Starting the application.")
    main()
