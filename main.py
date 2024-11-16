from datetime import datetime
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler

from src.news_fetcher.constants import QUERIES, UNAVAILABLE_ARTICLE_VALUES
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
        pages = fetcher.fetch_news(QUERIES)
        logging.info(f"Fetched {len(pages)} pages.")

        # Publish each article to Kafka
        for articles in pages:
            # Check if the current element (articles) is a valid list of articles
            if _is_valid_article_list(articles):
                for article in articles:
                    # Create a message by filtering out unavailable values
                    message = {key: value for key, value in article.items() if value not in UNAVAILABLE_ARTICLE_VALUES}

                    try:
                        producer.send_message(message)
                        logging.debug(f"Message sent to Kafka: {message['title']}")
                    except Exception as e:
                        logging.error(f"Error sending message to Kafka: {e}")

        logging.info("News fetched and published to Kafka successfully.")
    except Exception as e:
        logging.error(f"Error in news fetcher service: {e}")

# Helper function to validate the structure of the articles list
def _is_valid_article_list(data):
    """
    Validates if the input data is a list of articles.
    Each article must be a dictionary containing at least the key 'article_id'.
    """
    return isinstance(data, list) and all(isinstance(article, dict) and 'article_id' in article for article in data)


def main():
    logging.info("Initializing the news ingestion pipeline.")

    # Initialize and start scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_publish_news, 'interval', minutes=15, next_run_time=datetime.now())
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
