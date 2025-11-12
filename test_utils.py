#!/usr/bin/env python3
"""Utilities for the GitHubOrgClient"""

import requests
from functools import wraps
from typing import Callable, Any, Dict, List, Union


def get_json(url: str) -> Dict:
    """Fetch JSON from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(method: Callable) -> Callable:
    """Decorator to memoize a method."""
    cache = {}

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = (method.__name__, str(args), str(kwargs))
        if key not in cache:
            cache[key] = method(self, *args, **kwargs)
        return cache[key]

    return wrapper


def access_nested_map(dct: Dict, path: Union[List, str]) -> Any:
    """
    Safely access nested dictionary keys using a path (list of keys or dot-separated string).
    Returns None if any key is missing.
    """
    if isinstance(path, str):
        path = path.split('.')

    for key in path:
        if isinstance(dct, dict) and key in dct:
            dct = dct[key]
        else:
            return None
    return dct