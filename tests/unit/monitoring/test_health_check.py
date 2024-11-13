import unittest
from unittest.mock import patch, MagicMock

# Mock the Settings class itself to avoid needing environment variables
with patch('src.config.settings.Settings') as MockSettings:
    MockSettings.return_value = MagicMock(
        NEWS_API_KEY='test_api_key',
        KAFKA_BOOTSTRAP_SERVERS='localhost:9092',
        KAFKA_TOPIC='test_topic'
    )
    from src.monitoring.health_check import check_health

class TestHealthCheck(unittest.TestCase):

    @patch('src.monitoring.health_check.KafkaProducerSingleton')
    def test_check_health_success(self, mock_kafka_producer):
        """
        Test that check_health returns 200 when Kafka connection is successful.
        """
        # Mock KafkaProducerSingleton instance and its producer connection
        mock_producer_instance = MagicMock()
        mock_producer_instance.producer.bootstrap_connected.return_value = True
        mock_kafka_producer.return_value = mock_producer_instance

        # Call the function
        status_code = check_health()

        # Assert the status code is 200, indicating success
        self.assertEqual(status_code, 200)

    @patch('src.monitoring.health_check.KafkaProducerSingleton')
    def test_check_health_failure(self, mock_kafka_producer):
        """
        Test that check_health returns 503 when Kafka connection fails.
        """
        # Mock KafkaProducerSingleton to raise an exception simulating a failed connection
        mock_kafka_producer.side_effect = Exception("Connection failed")

        # Call the function
        status_code = check_health()

        # Assert the status code is 503, indicating failure
        self.assertEqual(status_code, 503)

if __name__ == "__main__":
    unittest.main()
