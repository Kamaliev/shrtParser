import logging
import os.path
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


class Database:

    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3')
        file = os.path.join(Path(__file__).parents[0], 'init.sql')
        with open(file, 'r') as f:
            sql = f.read()
        for q in sql.split(';'):
            self.execute(q)

    def execute(self, q, *args):

        cur = self.conn.cursor()

        try:
            cur.execute(q, args)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(e)
            self.conn.rollback()
        finally:
            cur.close()

    def close(self):
        self.conn.close()
