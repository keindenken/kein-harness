"""Application startup.

Everything the app does on launch happens here, in `start()`, before the window
is shown. It is the only place that runs once per launch.
"""

import sys

from . import db


def start():
    connection = db.connect()
    db.initialise(connection)
    return connection


def main(argv=None):
    argv = sys.argv if argv is None else argv
    connection = start()
    count = connection.execute("SELECT count(*) FROM notes").fetchone()[0]
    print(f"Marginalia: {count} notes in {db.database_path()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
