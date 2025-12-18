import os

from configs.config import DB_CONFIG

DB_DRIVER = None
try:
    import mariadb
    DB_DRIVER = 'mariadb'
except Exception:
    import sqlite3
    DB_DRIVER = 'sqlite'

DB_PATH = os.path.join(os.path.dirname(__file__), 'hms.db')


def _paramstyle():
    """Return the appropriate parameter placeholder for the current DB driver."""
    return "%s" if DB_DRIVER == 'mariadb' else "?"


def get_conn():
    if DB_DRIVER == 'mariadb':
        return mariadb.connect(
            host=DB_CONFIG.get('host', '127.0.0.1'),
            port=int(DB_CONFIG.get('port', 3306)),
            user=DB_CONFIG.get('user'),
            password=DB_CONFIG.get('password'),
            database=DB_CONFIG.get('database')
        )
    else:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn


def dict_from_row(row):
    try:
        return dict(row)
    except Exception:
        return dict(row)
