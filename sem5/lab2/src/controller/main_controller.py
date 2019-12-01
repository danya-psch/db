from view import View
from model import *
from controller.default_values import *
import psycopg2


class MainController(object):
    def __init__(self, connection):
        from controller import Controller
        self._connection = connection
        self._cursor = self._connection.cursor()
        self._game_controller = Controller(TypeOfTable.GAME, self, connection)
        self._player_controller = Controller(TypeOfTable.PLAYER, self, connection)
        self._developer_company_controller = Controller(TypeOfTable.DEVELOPER_COMPANY, self, connection)
        self._programmer_controller = Controller(TypeOfTable.PROGRAMMER, self, connection)
        self._developer_company__game_controller = Controller(TypeOfTable.DEVELOPER_COMPANY__GAME, self, connection)
        self._player__game_controller = Controller(TypeOfTable.PLAYER__GAME, self, connection)

    def start(self):
        while True:
            list_menu = ['CRUD operations with relations', 'Batch generation of "randomized" data',
                         'Search by multiple attributes of two entities', 'Full text search', "Exit"]
            menu_result = self.make_choice(list_menu, 'Main menu')

            if menu_result == 0:
                self.crud_operations()
            elif menu_result == 1:
                self.batch_generation_data()
            elif menu_result == 2:
                self.search_multiple_attr()
            elif menu_result == 3:
                self.choose_fulltext_search()
            elif menu_result == 4:
                break

    def close(self):
        return None

    def crud_operations(self):
        while True:
            list_menu = ['Game', 'Player', 'Developer company', 'Programmer', 'Developer company - game', 'Player - game', 'Back']
            menu_result = self.make_choice(list_menu, 'CRUD operations with relations')

            if menu_result == 0:
                self._game_controller.choose_operation()
            elif menu_result == 1:
                self._player_controller.choose_operation()
            elif menu_result == 2:
                self._developer_company_controller.choose_operation()
            elif menu_result == 3:
                self._programmer_controller.choose_operation()
            elif menu_result == 4:
                self._developer_company__game_controller.choose_operation()
            elif menu_result == 5:
                self._player__game_controller.choose_operation()
            elif menu_result == 6:
                break

    def batch_generation_data(self):
        self._game_controller.model.create_items(default_games)
        self._developer_company_controller.model.create_items(default_developer_companies)
        self._player_controller.model.create_items(default_players)
        self._programmer_controller.model.create_items(default_programmers)
        self._developer_company__game_controller.model.create_items(default_developer_company__game)
        self._player__game_controller.model.create_items(default_player__game)
        View.show_text('Successfully done')

    def search_multiple_attr(self):
        try:
            self._programmer_controller.show_all()
            View.print_line()
            user_input = self.get_value("Print enumeration: ", str)
            list_of_enum = (user_input[:-1][1:]).split()
            str_of_enum = ''.join([f"\'{item}\', " for item in list_of_enum])
            str_of_enum = str_of_enum[:-2]
            top_line = self.get_value("Print top_line for search: ", int)
            bottom_line = top_line + 1
            while top_line <= bottom_line:
                bottom_line = self.get_value("Print bottom_line for search: ", int)
            self._cursor.execute(f"SELECT * FROM programmer t1 INNER JOIN developer_company t2 ON "
                                 f"t1.developer_company_id = t2.id WHERE t2.name IN ({str_of_enum}) "
                                 f"AND t1.salary < {top_line} AND t1.salary > {bottom_line}")

            table = self._cursor.fetchall()
            if table is None:
                raise Exception('There is no items ')

            View.show_items(table) if len(table) > 1 else View.show_item(table)
        except (Exception, psycopg2.Error) as e:
            View.show_error(str(e))

    def choose_fulltext_search(self):
        while True:
            self._developer_company_controller.show_all()
            View.print_line()
            list_menu = ['Whole phrase', 'Required word occurrence', 'Back']
            menu_option = self.make_choice(list_menu, 'Full text search')
            if menu_option == 0:
                self.fulltext_search(True)
            elif menu_option == 1:
                self.fulltext_search(False)
            elif menu_option == 2:
                break

    def fulltext_search(self,  is_order_important: bool):
        try:
            query = self.get_value('Enter query: ', str)
            query_whole_text = f"SELECT * FROM developer_company, phraseto_tsquery(\'english\', \'{query}\') AS q WHERE to_tsvector('english', description) @@ q"
            query_including = f"SELECT * FROM developer_company, plainto_tsquery(\'english\', \'{query}\') AS q WHERE to_tsvector('english', description) @@ q"
            self._cursor.execute(query_whole_text if is_order_important else query_including)
            rows = self._cursor.fetchall()
            if list(rows):
                View.show_items(rows)
            else:
                raise Exception("There are no items")
        except (Exception, psycopg2.Error) as e:
            View.show_error(str(e))

    @staticmethod
    def make_choice(menu_list: list, name_of_menu: str):
        try:
            View.draw_menu(menu_list, name_of_menu)
            return MainController.get_uint_value("Make your choice: ", len(menu_list))

        except Exception as e:
            View.show_error(str(e))

    @staticmethod
    def get_uint_value(msg: str, top_line: int = None):
        while True:
            number = input(msg)
            if number.isdigit():
                number = int(number)
                if top_line is None or 0 <= number < top_line:
                    return number

    @staticmethod
    def get_value(msg: str, type_of_var):
        is_date = True if type_of_var == date else False
        while True:
            try:
                usr_input = input(f"{msg[:-2]} in YYYY-MM-DD format: " if is_date else msg)
                if type_of_var == str:
                    return f"\'{type_of_var(usr_input)}\'"
                elif type_of_var == date:
                    year, month, day = map(int, usr_input.split('-'))
                    return f"\'{date(year, month, day)}\'"
                else:
                    return type_of_var(usr_input)
            except Exception as e:
                View.show_error(str(e))




