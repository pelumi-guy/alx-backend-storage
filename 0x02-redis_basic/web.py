#!/usr/bin/env python3
"""
5. Implementing an expiring web cache and tracke
"""
from pprint import pprint
import redis
import requests
from functools import wraps
from datetime import timedelta


r = redis.Redis()


def url_access_count(method):
    """decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        redis.incr(f"count:{url}")
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        html_content = method(url)

        # r.set(key, html_content, ex=10)
        # r.expire(key, 10)
        r.setex(key, timedelta(seconds=10), value=html_content)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """
    A function that obtains the HTML content of a particular URL and returns it
    """
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    # get_page('http://slowwly.robertomurray.co.uk')
    page = get_page('http://www.example.com')
    pprint(page)
