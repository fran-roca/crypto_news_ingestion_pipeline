import requests
import time
import logging
from .constants import API_URL, QUERIES, MAX_CREDITS, REQUEST_INTERVAL, RATE_LIMIT_PAUSE

class NewsDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.credits_used = 0

    def fetch_news(self, query, page=None):
        if self.credits_used >= MAX_CREDITS:
            logging.warning("Daily API credit limit reached. Stopping requests.")
            return []

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
                time.sleep(RATE_LIMIT_PAUSE)
                return self.fetch_news(query, page)  # Retry after delay if rate limit is hit
            response.raise_for_status()
            self.credits_used += 1
            data = response.json()
            return data.get('results', []), data.get('nextPage')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching news: {e}")
            return [], None

    def fetch_all_news(self):
        all_articles = []
        for query in QUERIES:
            page = None
            while self.credits_used < MAX_CREDITS:
                articles, next_page = self.fetch_news(query, page)
                if not articles:
                    break
                all_articles.extend(articles)
                page = next_page  # Use nextPage token for subsequent requests
                if not next_page:
                    break
                time.sleep(REQUEST_INTERVAL)  # Wait between requests
        return all_articles
