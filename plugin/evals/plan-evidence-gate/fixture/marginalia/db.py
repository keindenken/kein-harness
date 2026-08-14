"""Connection and schema for the note library."""

import os
import sqlite3
import sys
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id         INTEGER PRIMARY KEY,
    title      TEXT NOT NULL,
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    tags       TEXT NOT NULL DEFAULT '[]'
);
CREATE INDEX IF NOT EXISTS notes_updated_at ON notes (updated_at);
"""


def library_directory():
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Marginalia"
    if sys.platform == "win32":
        return Path(os.environ["APPDATA"]) / "Marginalia"
    return Path.home() / ".local" / "share" / "marginalia"


def database_path():
    return library_directory() / "notes.db"


def connect(path=None):
    connection = sqlite3.connect(path or database_path())
    connection.row_factory = sqlite3.Row
    return connection


def initialise(connection):
    connection.executescript(SCHEMA)
    connection.commit()
