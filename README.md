# Python Context and Async Operations

## Overview
This project explores advanced Python techniques for managing database connections using context managers and asynchronous programming.

### Learning Objectives
- Implement class-based context managers (`__enter__`, `__exit__`)
- Perform asynchronous database queries using `aiosqlite`
- Run concurrent operations with `asyncio.gather`

### Files
- `0-databaseconnection.py` — Custom class-based context manager
- `1-execute.py` — Reusable query executor context manager
- `3-concurrent.py` — Asynchronous concurrent database queries

### Tools
- `sqlite3`
- `aiosqlite`
- `asyncio`

### Example Usage
```bash
python3 0-databaseconnection.py
python3 1-execute.py
python3 3-concurrent.py
