import pytest
from src.news_data_fetcher import NewsDataFetcher

def test_fetch_news(mocker):
    mocker.patch("requests.get")
    fetcher = NewsDataFetcher("test_api_key")
    articles = fetcher.fetch_news("Bitcoin")
    assert articles is not None
