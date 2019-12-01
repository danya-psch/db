from model.model_config import *


class Model(object):
    def __init__(self, item_type: TypeOfTable, connection):
        self._item_type = item_type
        self._connection = connection
        self._cursor = connection.cursor()
        self._fields = {}

    def __del__(self):
        self._cursor.close()

    @property
    def type(self):
        return self._item_type

    @type.setter
    def type(self, new_type):
        self.type = new_type

    @property
    def fields(self):
        return self._fields

    def create_item(self, fields_lits: dict):
        self._check_fields(fields_lits)
        if self._check_already_exists(fields_lits) is not None:
            raise Exception('item already exist')

        fields = ''.join([str(item) + ', ' if str(item)[:3] != '___' else str(item)[3:] + ', ' for item in fields_lits.keys()])
        fields = fields[:-2]

        values = ''.join([("%s, " % item) for item in fields_lits.values()])
        values = values[:-2]

        self._cursor.execute(f"INSERT INTO {self.type.value[0]} ({fields}) VALUES ({values});")
        self._connection.commit()

    def create_items(self, items: list):
        self.truncate_table()
        for item in items:
            self.create_item(item)

    def read_item(self, id: int):
        self._cursor.execute(f"SELECT * FROM public.{self.type.value[0]} WHERE id = {id};")
        row = self._cursor.fetchone()
        return row

    def read_all_items(self):
        self._cursor.execute(f"SELECT * FROM public.{self.type.value[0]};")
        table = self._cursor.fetchall()
        return table

    def update_item(self, id: int, fields_lits: dict):
        self._check_fields(fields_lits)
        '''new_values = ''.join([
            str(field) + ' = ' + str(value) + ', ' for field, value in zip(fields_lits.keys(), fields_lits.values())
        ])
        new_values = new_values[:-2]'''
        if self._check_already_exists(fields_lits) is not None:
            raise Exception('item already exist')

        self._cursor.execute(f"UPDATE {self.type.value[0]} SET {self._create_list_fields_with_values(fields_lits, ', ')} WHERE id = {id};")
        self._connection.commit()

    def delete_item(self, id: int):
        self._cursor.execute(f"DELETE FROM {self.type.value[0]} WHERE id = {id};")
        self._connection.commit()

    def truncate_table(self):
        additional_table = []
        for key, values in relation_of_tables.items():
            if self.type.value[0] in values:
                additional_table.append(str(key))
        query = f"TRUNCATE TABLE {self.type.value[0]}"
        if len(additional_table) > 0:
            query += f", {''.join([str(item) + ', ' for item in additional_table])[:-2]}"
        self._cursor.execute(query)
        self._connection.commit()

    def _check_fields(self, fields_lits: dict):

        for field, value in fields_lits.items():
            if '___' in str(field)[:3]:
                if self.check_id(value, relation_field_to_table[str(field)[3:]].value[0]) is None:
                    raise Exception('There is no row with such id')
            elif str(field) == 'id':
                if self.check_id(value, self.type.value[0]) is not None:
                    raise Exception('Cant insert row with such id, it already exists ')

    def check_id(self, id: int, table):
        self._cursor.execute(f"SELECT * FROM public.{table} WHERE id = {id};")
        return self._cursor.fetchone()

    def _check_already_exists(self, fields_lits: dict):
        self._cursor.execute(f"SELECT * FROM public.{self.type.value[0]} WHERE {self._create_list_fields_with_values(fields_lits, ' AND ')};")
        return self._cursor.fetchone()

    @staticmethod
    def _create_list_fields_with_values(fields_lits : dict, tail: str):
        new_values = ''.join([
            Model.get_name_of_field(str(field)) + ' = ' + str(value) + tail for field, value in zip(fields_lits.keys(), fields_lits.values())
        ])
        return new_values[:-len(tail)]

    @staticmethod
    def get_name_of_field(name_of_field):
        return name_of_field if name_of_field[:3] != '___' else name_of_field[3:]




