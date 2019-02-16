
from tinydb import TinyDB, Query

import tempfile
import scraper

class CPDatabase():

    def __init__(self, location=None):
        if location is None:
            self.db_filename = 'chicken-parm.json'
        else:
            self.db_filename = location

        self.db = TinyDB(self.db_filename)
        self.table = self.db.table('cp')

    def get_update(self):
        update = scraper.get_menu()
        self.table.upsert({'date': update}, Query().date.exists())

    def get_menu(self):
        menu = Query()
        item = self.table.search(menu.date.exists())
        return str(item[0]['date'])
