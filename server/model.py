import sqlite3

REAL_DELETE = 1
SHORT_FORM = 1
WITH_DEACTIVATED = 1
DEACTIVATED_ONLY = 2
ACTIVE_ONLY = 0

class MakeSql:
    def __init__(self, model: dict, con: sqlite3.Connection) -> None:
        self.model = model
        self.table_names = tuple(model.keys())
        self.con = con
        self.con.row_factory = sqlite3.Row
        self.cur = con.cursor()

    def get(self, table_name: str, id: int, extended=True):
        if table_name not in self.table_names:
            return {'error': 'Table not exist', 'value': {}}
        if extended:
            add_sel, add_join = self.create_addons(table_name)
            s = f'SELECT {table_name}.*{add_sel} FROM {table_name}{add_join} WHERE {table_name}.id = ?'
        else:
            s = f'SELECT * FROM {table_name} WHERE id = ?'
        self.cur.execute(s, (id,))
        res = self.cur.fetchone()
        res = dict(res)
        return {'error': '', 'value': res}

    def get_all(self, table_name: str, extended=True, get_all=0):
        if table_name not in self.table_names:
            return {'error': 'Table not exist', 'value': {}}
        if extended:
            add_sel, add_join = self.create_addons(table_name)
            s = f'SELECT {table_name}.*{add_sel} FROM {table_name}{add_join}'
            if get_all == DEACTIVATED_ONLY:
                s += f' WHERE {table_name}.is_active = 0'
            elif get_all == ACTIVE_ONLY:
                s += f' WHERE {table_name}.is_active = 1'
        else:
            s = f'SELECT * FROM {table_name}'
            if get_all == DEACTIVATED_ONLY:
                s += ' WHERE is_active = 0'
            elif get_all == ACTIVE_ONLY:
                s += ' WHERE is_active = 1'
        self.cur.execute(s)
        res_list = self.cur.fetchall()
        res = []
        for r in res_list:
            res.append(dict(r))
        return {'error': '', 'value': res}

    def create(self, table_name: str, data: dict):
        if table_name not in self.table_names:
            return {'error': 'Table not exist', 'value': {}}
        fields = self.model[table_name]['fields']
        templ = ('?, ' * (len(fields)))[:-2]
        s = f"INSERT INTO {table_name} VALUES ({templ})"
        values = []
        for field in fields.keys():
            if field == 'id':
                values.append(None)
            else:
                values.append(data[field])
        self.cur.execute(s, values)
        self.con.commit()
        data['id'] = self.cur.lastrowid
        return {'error': '', 'value': data}

    def update(self, table_name: str, data: dict, id: int):
        if table_name not in self.table_names:
            return {'error': 'Table not exist', 'value': {}}
        fields = self.model[table_name]['fields']
        values = []
        fields_str = ''
        for field in fields.keys():
            if field == 'id':
                continue
            fields_str += f'{field} = ?, '
            values.append(data[field])
        s = f'UPDATE {table_name} SET {fields_str[:-2]} WHERE id = ?;'
        values.append(id)
        self.cur.execute(s, values)
        self.con.commit()
        return {'error': '', 'value': 'Sucsess'}

    def deactivate(self, table_name: str, id: int):
        if table_name not in self.table_names:
            return {'error': 'Table not exist', 'value': {}}
        s = f'UPDATE {table_name} SET is_active = 0 WHERE id = ?'
        self.cur.execute(s, (id,))
        self.con.commit()
        return {'error': '', 'value': 'Sucsess'}

    def delete(self, table_name: str, id: int):
        if table_name not in self.table_names:
            return {'error': 'Table not exist', 'value': {}}
        s = f'DELETE FROM {table_name} WHERE id = ?'
        self.cur.execute(s, (id,))
        self.con.commit()
        return {'error': '', 'value': 'Sucsess'}

    #===================================================

    def create_addons(self, table_name):
        add_sel = ''
        add_join = ''
        fields = self.model[table_name]['fields'].keys()
        for f in fields:
            if not f.endswith('_id'):
                continue

            foring_table_name = '_'.join(f.split('_')[:-1])

            if foring_table_name == table_name:
                add_sel += f', IFNULL({foring_table_name[:3]}.name, "") as {foring_table_name}'
                add_join += f'\n\tLEFT JOIN {foring_table_name} AS {foring_table_name[:3]} ON {table_name}.{f} = {foring_table_name[:3]}.id'
            else:
                add_sel += f', IFNULL({foring_table_name}.name, "")'
                add_join += f'\n\tLEFT JOIN {foring_table_name} ON {table_name}.{f} = {foring_table_name}.id'

        return add_sel, add_join


    def create_order(self, contact, contact_type, svg_data):
        print("contact", contact)
        print("contact_type", contact_type)
        with open ('maket_new.svg', "w") as f:
            f.write(svg_data)
        return {'error': '', 'value': 'Sucsess'}
