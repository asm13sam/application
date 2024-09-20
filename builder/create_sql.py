import json
import sqlite3
from barcode import EAN13


class SqlCreator:
    def __init__(self, model: dict, cur: sqlite3.Cursor) -> None:
        self.model = model
        self.cur = cur

    def create_table(self, table_name: str, table_fields: dict):
        print('creating', table_name)
        s = f'CREATE TABLE IF NOT EXISTS {table_name}\n('
        for k, v in table_fields.items():
            print(k, v)
            d = v['def']
            if k == 'id':
                s += '\n\tid INTEGER PRIMARY KEY AUTOINCREMENT,'
            elif type(d) == int:
                s += f'\n\t{k} INT NOT NULL,'
            elif type(d) == float:
                s += f'\n\t{k} REAL NOT NULL,'
            elif type(d) == bool:
                s += f'\n\t{k} BOOL NOT NULL,'
            else:
                s += f'\n\t{k} TEXT NOT NULL,'
        s = s[:-1] + '\n);\n'
        return s

    def make_sql(self):
        s = ''
        for table_name in self.model:
            s += f'DROP TABLE IF EXISTS {table_name};\n'
            s += self.create_table(table_name, self.model[table_name]['fields'])
        self.cur.executescript(s)
