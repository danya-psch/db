from model import *
from controller.main_controller import MainController
from view import View
from model.model_config import list_of_fields
from typing import Type
from sqlalchemy.orm import Session

import psycopg2


class Controller:
    def __init__(self, type_of_table: TypeOfTable, session: Session, cls: Type, main_controller):
        self._main_controller = main_controller
        self._model = Model(type_of_table, session, cls)
        self._type_of_table = type_of_table
        self._cls = cls


    @property
    def model(self):
        return self._model

    def show(self, id: int):
        try:
            item = self._model.read_item(id)
            if item is None:
                raise Exception('There is no item with that id ')
            View.show_item(item, self._type_of_table)
        except Exception as e:
            View.show_error(str(e))
            self._model.rollback()


    def show_all(self):
        try:
            table = self._model.read_all_items()
            if table is None:
                raise Exception('There is no items')
            View.show_items(table, self._type_of_table)
        except Exception as e:
            View.show_error(str(e))
            self._model.rollback()

    def insert(self):
        try:
            self._model.create_item(self._get_values_for_model())
        except Exception as e:
            View.show_error(str(e))
            self._model.rollback()

    def update(self, id: int):
        try:
            if not self._model.check_row_exist(id):
                raise Exception('Such a row does not exist')
            self._model.update_item(id, self._get_values_for_model())
        except (Exception, psycopg2.Error) as e:
            View.show_error(str(e))
            self._model.rollback()

    def delete(self, id: int):
        try:
            if not self._model.check_row_exist(id):
                raise Exception('Such a row does not exist')
            self._model.delete_item(id)
        except (Exception, psycopg2.Error) as e:
            View.show_error(str(e))
            self._model.rollback()

    def choose_operation(self):
        while True:
            check = self._type_of_table == TypeOfTable.PLAYER__GAME or self._type_of_table == TypeOfTable.DEVELOPER_COMPANY__GAME;
            list_operations = ['Create', 'Read', 'Update', 'Delete', 'List all', 'Back']
            if check:
                list_operations = ['Create', 'List all', 'Back']
            operation = self._main_controller.make_choice(list_operations, self._type_of_table.value[0])
            if check:
                if operation == 0:
                    self.insert()
                elif operation == 1:
                    self.show_all()
                elif operation == 2:
                    break
            else:
                if operation == 0:
                    self.insert()
                elif operation == 1:
                    self.show(MainController.get_uint_value("Print id: "))
                elif operation == 2:
                    self.update(MainController.get_uint_value("Print id: "))
                elif operation == 3:
                    self.delete(MainController.get_uint_value("Print id: "))
                elif operation == 4:
                    self.show_all()
                elif operation == 5:
                    break

    def _get_values_for_model(self):
        input_values = {}
        exact_list_of_fields = list_of_fields[self._type_of_table]
        for name_of_field, type_of_field in exact_list_of_fields.items():
            if name_of_field != 'id':
                input_values[name_of_field] = MainController.get_value(f"Enter {Model.get_name_of_field(name_of_field)}: ", type_of_field)
        return input_values
