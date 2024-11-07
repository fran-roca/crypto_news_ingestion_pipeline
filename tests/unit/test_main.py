import unittest
from unittest.mock import patch, MagicMock

# Patch Settings directly before importing main module
with patch('src.config.settings.Settings') as MockSettings:
    # Configure the mock Settings to provide required fields
    MockSettings.return_value = MagicMock(
        NEWS_API_KEY="dummy_api_key",
        KAFKA_BOOTSTRAP_SERVERS="localhost:9092",
        KAFKA_TOPIC="test_topic"
    )
    # Import the function to be tested after patching
    from main import fetch_and_publish_news

class TestMain(unittest.TestCase):

    @patch('main.get_settings')
    @patch('main.NewsDataFetcher')
    @patch('main.KafkaProducerSingleton')
    def test_fetch_and_publish_news(self, mock_kafka_producer, mock_news_fetcher, mock_get_settings):
        # Set up mock for get_settings to return mock settings
        mock_settings = MagicMock()
        mock_settings.NEWS_API_KEY = "dummy_api_key"
        mock_get_settings.return_value = mock_settings

        # Configure NewsDataFetcher mock
        mock_fetcher_instance = MagicMock()
        mock_fetcher_instance.fetch_all_news.return_value = [
            {'title': 'News Title', 'description': 'News Desc', 'url': 'http://news.url', 'publishedAt': '2023-01-01'}
        ]
        mock_news_fetcher.return_value = mock_fetcher_instance

        # Configure KafkaProducerSingleton mock
        mock_producer_instance = MagicMock()
        mock_kafka_producer.return_value = mock_producer_instance

        # Call the function
        fetch_and_publish_news()

        # Assert that send_message was called once with expected data
        mock_producer_instance.send_message.assert_called_once_with({
            'title': 'News Title',
            'description': 'News Desc',
            'url': 'http://news.url',
            'publishedAt': '2023-01-01'
        })

if __name__ == "__main__":
    unittest.main()
