"""Search over the note library."""

from . import db

FIND = """
SELECT id, title, body, updated_at
  FROM notes
 WHERE title LIKE :pattern OR body LIKE :pattern
 ORDER BY updated_at DESC
"""


def search(term, connection=None):
    """Every note whose title or body contains `term`, newest first.

    There is no ranking here. The caller gets rows in recency order and has no way
    to tell a title hit from a body hit, or one match from twenty.
    """
    connection = connection or db.connect()
    return connection.execute(FIND, {"pattern": f"%{term}%"}).fetchall()
