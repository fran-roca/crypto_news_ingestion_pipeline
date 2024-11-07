API_URL = "https://newsdata.io/api/1/news"
QUERIES = ['Bitcoin', 'Ethereum', 'cryptocurrency']
MAX_ARTICLES = 2000
ARTICLES_PER_PAGE = 10
MAX_CREDITS = 200  # Free tier daily limit
REQUEST_INTERVAL = 420  # 7 minutes between each request in seconds
RATE_LIMIT_PAUSE = 900  # 15-minute pause when hitting rate limit