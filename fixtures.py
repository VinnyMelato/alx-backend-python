#!/usr/bin/env python3
"""Contains fixtures for client unit tests"""

org_payload = {
    "login": "google",
    "id": 1342004,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=",
    "repos_url": "https://api.github.com/orgs/google/repos",
}

repos_payload = [
    {"id": 7697149, "name": "autoparse", "private": False},
    {"id": 7776515, "name": "build-debian-cloud", "private": False},
]

expected_repos = ["autoparse", "build-debian-cloud"]

apache2_repos = [
    {"id": 7697149, "name": "autoparse", "license": {"key": "apache-2.0"}},
    {"id": 7776515, "name": "build-debian-cloud", "license": {"key": "apache-2.0"}},
]
