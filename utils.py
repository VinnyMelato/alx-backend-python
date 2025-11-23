#!/usr/bin/env python3
"""utils.py - helper functions and decorators"""

import requests
from functools import wraps


def get_json(url: str) -> dict:
    """Fetch JSON content from a URL"""
    response = requests.get(url)
    return response.json()


def memoize(method):
    """Decorator to cache the result of a method"""

    @wraps(method)
    def memoized(self):
        """Store the result once and reuse it"""
        attr_name = f"_{method.__name__}"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return memoized
