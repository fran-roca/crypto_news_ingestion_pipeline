import requests
import time
import logging
from .constants import API_URL, MAX_CREDITS, RATE_LIMIT_PAUSE

class NewsDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.credits_used = 0

    def fetch_news(self, query, page=None, retry_count=0, max_retries=3):
        if self.credits_used >= MAX_CREDITS:
            logging.warning("Daily API credit limit reached. Stopping requests.")
            return [], None

        params = {
            'apikey': self.api_key,
            'q': query,
            'language': 'en',
        }
        if page:
            params['page'] = page

        try:
            response = requests.get(API_URL, params=params)
            if response.status_code == 429:
                logging.warning("Rate limit hit. Pausing before retry.")
                if retry_count < max_retries:
                    time.sleep(RATE_LIMIT_PAUSE)
                    return self.fetch_news(query, page, retry_count + 1)  # Retry with incremented count
                else:
                    logging.error("Max retries reached. Skipping request.")
                    return [], None
            response.raise_for_status()
            self.credits_used += 1
            data = response.json()
            return data.get('results', []), data.get('nextPage')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching news: {e}")
            return [], None  # Ensure this catches all exceptions and returns expected values

