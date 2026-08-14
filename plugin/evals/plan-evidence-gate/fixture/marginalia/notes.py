"""Create, edit and delete notes.

Every write to the `notes` table goes through this module. Nothing else in the
application issues INSERT, UPDATE or DELETE against it.
"""

import json
from datetime import datetime, timezone

from . import db

INSERT = """
INSERT INTO notes (title, body, created_at, updated_at, tags)
VALUES (:title, :body, :now, :now, :tags)
"""

UPDATE = """
UPDATE notes SET title = :title, body = :body, updated_at = :now WHERE id = :id
"""

DELETE = "DELETE FROM notes WHERE id = :id"


def _now():
    return datetime.now(timezone.utc).isoformat()


def create(title, body, tags=(), connection=None):
    connection = connection or db.connect()
    with connection:
        cursor = connection.execute(
            INSERT, {"title": title, "body": body, "now": _now(), "tags": json.dumps(list(tags))})
    return cursor.lastrowid


def update(note_id, title, body, connection=None):
    connection = connection or db.connect()
    with connection:
        connection.execute(UPDATE, {"id": note_id, "title": title, "body": body, "now": _now()})


def delete(note_id, connection=None):
    connection = connection or db.connect()
    with connection:
        connection.execute(DELETE, {"id": note_id})
