from model.model_config import *

from sqlalchemy.orm import Session
from sqlalchemy import asc
from typing import Type
from model.game import Game
from model.player import Player
from model.developer_company import DeveloperCompany
from model.programmer import Programmer
from model.developer_company__game import DeveloperCompany__Game
from model.player__game import Player__Game


class Model(object):
    def __init__(self, item_type: TypeOfTable, session: Session, cls: Type):
        self._item_type = item_type
        self._session = session
        self._cls = cls

    @property
    def type(self):
        return self._item_type

    @type.setter
    def type(self, new_type):
        self.type = new_type

    @property
    def session(self):
        return self._session

    def create_item(self, fields_list: dict):
        self._check_fields(fields_list)
        self._session.add(self._cls.create_obj(fields_list))
        self._commit_or_rollback_on_failure()

    def create_items(self, items: list):
        self.truncate_table()
        for item in items:
            self.create_item(item)

    def read_item(self, id: int):
        item = self._session.query(self._cls).get(id)
        if item is None:
            raise Exception(f"No item with such id {id} was found")
        return item

    def read_all_items(self):
        items = self._session.query(self._cls).order_by(order_by[self._item_type] if self._item_type in order_by else asc('id')).offset(0).limit(None).all()
        return items

    def update_item(self, id: int, fields_list: dict):
        new_field_list = self._check_fields(fields_list)
        self._session.query(self._cls).filter_by(**{'id': id}).update(new_field_list)
        self._commit_or_rollback_on_failure()

    def delete_item(self, id: int):
        for key, values in relation_of_tables.items():
            if self.type.value[0] in values:
                self._session.query(class_to_type_relation[key]).filter_by(**{f"{self.type.value[0]}_id": id}).delete()
        self._session.query(self._cls).filter_by(**{'id': id}).delete()
        self._commit_or_rollback_on_failure()

    def truncate_table(self):
        additional_table = []
        for key, values in relation_of_tables.items():
            if self.type.value[0] in values:
                additional_table.append(str(key.value[0]))
        query = f"TRUNCATE TABLE {self.type.value[0]}"
        if len(additional_table) > 0:
            query += f", {''.join([str(item) + ', ' for item in additional_table])[:-2]}"
        self._session.execute(query)

    def _commit_or_rollback_on_failure(self):
        try:
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def rollback(self):
        self._session.rollback()

    @staticmethod
    def get_name_of_field(name_of_field):
        return name_of_field if name_of_field[:3] != '___' else name_of_field[3:]

    def _check_fields(self, fields_lits: dict):
        new_dict = {}
        for field, value in fields_lits.items():
            if '___' in str(field)[:3]:
                if not self.check_row_exist_in_table(value, relation_field_to_table[str(field)[3:]].value[0]):
                    raise Exception('There is no row with such id')
                new_dict[field[3:]] = value
            elif str(field) == 'id':
                if self.check_row_exist_in_table(value, self.type.value[0]):
                    raise Exception('Cant insert row with such id, it already exists ')
        for field, value in new_dict.items():
            del fields_lits[f"___{field}"]
            fields_lits[field] = value
        return fields_lits

    def check_row_exist(self, id: int):
        return self._session.query(self._cls).filter_by(**{'id': id}).scalar() is not None

    def check_row_exist_in_table(self, id: int, table):
        cls = self._cls
        if table == TypeOfTable.PLAYER.value[0]:
            cls = Player
        elif table == TypeOfTable.GAME.value[0]:
            cls = Game
        elif table == TypeOfTable.DEVELOPER_COMPANY.value[0]:
            cls = DeveloperCompany
        elif table == TypeOfTable.PROGRAMMER.value[0]:
            cls = Programmer
        return self._session.query(cls).filter_by(**{'id': id}).scalar() is not None


'''
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
'''
