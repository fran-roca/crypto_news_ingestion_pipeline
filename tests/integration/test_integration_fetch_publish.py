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

class TestIntegrationFetchAndPublish(unittest.TestCase):

    @patch('main.get_settings')
    @patch('main.NewsDataFetcher')
    @patch('main.KafkaProducerSingleton')
    def test_fetch_and_publish_news_integration(self, mock_kafka_producer, mock_news_fetcher, mock_get_settings):
        # Setup mock for settings
        mock_settings = MagicMock()
        mock_settings.NEWS_API_KEY = "dummy_api_key"
        mock_get_settings.return_value = mock_settings

        # Setup mock for NewsDataFetcher
        mock_fetcher_instance = MagicMock()
        # Simulate fetching multiple articles
        mock_fetcher_instance.fetch_all_news.return_value = [
            {'title': 'News Title 1', 'description': 'Description 1', 'url': 'http://news.url/1', 'publishedAt': '2023-01-01'},
            {'title': 'News Title 2', 'description': 'Description 2', 'url': 'http://news.url/2', 'publishedAt': '2023-01-02'}
        ]
        mock_news_fetcher.return_value = mock_fetcher_instance

        # Setup mock for Kafka producer
        mock_producer_instance = MagicMock()
        mock_kafka_producer.return_value = mock_producer_instance

        # Run the integration function
        fetch_and_publish_news()

        # Assert NewsDataFetcher is called to fetch all news
        mock_fetcher_instance.fetch_all_news.assert_called_once()

        # Assert Kafka producer's `send_message` method is called for each article
        self.assertEqual(mock_producer_instance.send_message.call_count, 2)
        # Check that each message was published with correct data
        calls = [
            unittest.mock.call({
                'title': 'News Title 1',
                'description': 'Description 1',
                'url': 'http://news.url/1',
                'publishedAt': '2023-01-01'
            }),
            unittest.mock.call({
                'title': 'News Title 2',
                'description': 'Description 2',
                'url': 'http://news.url/2',
                'publishedAt': '2023-01-02'
            })
        ]
        mock_producer_instance.send_message.assert_has_calls(calls, any_order=True)

if __name__ == "__main__":
    unittest.main()
