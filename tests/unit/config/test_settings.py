import unittest
from src.config.settings import get_settings
from unittest.mock import patch

class TestSettings(unittest.TestCase):

    @patch.dict('os.environ', {
        'NEWS_API_KEY': 'test_api_key',
        'KAFKA_BOOTSTRAP_SERVERS': 'localhost:9092',
        'KAFKA_TOPIC': 'test_topic'  # Add this line
    })
    def test_get_settings(self):
        settings = get_settings()
        self.assertEqual(settings.NEWS_API_KEY, 'test_api_key')
        self.assertEqual(settings.KAFKA_BOOTSTRAP_SERVERS, 'localhost:9092')
        self.assertEqual(settings.KAFKA_TOPIC, 'test_topic')  # Check this value as well

if __name__ == "__main__":
    unittest.main()
