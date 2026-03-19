import pytest
from api.services.reddit_service import RedditService

def test_extract_tickers():
    import os
    os.environ["REDDIT_CLIENT_ID"] = "dummy"
    os.environ["REDDIT_CLIENT_SECRET"] = "dummy"
    os.environ["REDDIT_USERNAME"] = "dummy"
    os.environ["REDDIT_PASSWORD"] = "dummy"
    service = RedditService()
    posts = [
        {"title": "I bought some AAPL today", "selftext": "Thinking about buying more MSFT."},
        {"title": "YOLO into GME", "selftext": "GME to the moon! AAPL is for boomers."},
        {"title": "What about TSLA?", "selftext": "TSLA is looking good. Also looking at MSFT."},
        {"title": "Just a normal post", "selftext": "Nothing to see here."},
        {"title": "I love the CEO of AAPL", "selftext": "AAPL AAPL AAPL!"} # CEO should be excluded
    ]

    tickers = service._extract_tickers(posts)

    # AAPL: 5 (1 + 1 + 3)
    # MSFT: 2 (1 + 1)
    # GME: 2 (1 + 1)
    # TSLA: 2 (1 + 1)

    assert "AAPL" in tickers
    assert tickers["AAPL"] == 6
    assert "MSFT" in tickers
    assert tickers["MSFT"] == 2
    assert "GME" in tickers
    assert tickers["GME"] == 2
    assert "TSLA" in tickers
    assert tickers["TSLA"] == 2

    # Excluded words shouldn't be here
    assert "CEO" not in tickers
    assert "YOLO" not in tickers
