import unittest
import requests
from unittest.mock import patch, MagicMock
from src.news_fetcher.news_data_fetcher import NewsDataFetcher


class TestNewsDataFetcher(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.api_key = "dummy_api_key"
        self.fetcher = NewsDataFetcher(self.api_key)

    @patch('src.news_fetcher.news_data_fetcher.requests.get')
    def test_fetch_news_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': [{'title': 'Sample News'}], 'nextPage': '2'}
        mock_get.return_value = mock_response

        articles, next_page = self.fetcher.fetch_news('Bitcoin')
        self.assertEqual(len(articles), 1)
        self.assertEqual(next_page, '2')

    @patch('src.news_fetcher.news_data_fetcher.requests.get')
    def test_fetch_news_rate_limit(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        with patch('time.sleep', return_value=None):  # Skip sleep for test
            articles, _ = self.fetcher.fetch_news('Bitcoin')
            self.assertEqual(articles, [])

    @patch('src.news_fetcher.news_data_fetcher.requests.get')  # Corrected patch path
    def test_fetch_news_exception(self, mock_get):
        # Set side_effect on mock_get to simulate a ConnectionError
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")

        # Call fetch_news and check it handles the exception gracefully
        articles, next_page = self.fetcher.fetch_news('Bitcoin')

        # Assert that an empty list and None are returned on exception
        self.assertEqual(articles, [])
        self.assertIsNone(next_page)


if __name__ == "__main__":
    unittest.main()
