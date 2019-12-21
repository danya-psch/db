from model.model_config import TypeOfTable, list_of_fields
from prettytable import PrettyTable


class View(object):

    @staticmethod
    def draw_menu(menu_list, name_of_menu: str):
        print(f"\n{name_of_menu}")
        number = 0
        for menu_item in menu_list:
            print(f" {number}: {menu_item}")
            number += 1

    @staticmethod
    def show_item(item, type_: TypeOfTable = TypeOfTable.NONE):
        print("Item:")
        # print(item)
        if type_ != TypeOfTable.NONE:
            t = PrettyTable(list_of_fields[type_])
            list_of_item = item.get_data()
            if len(list_of_fields[type_]) < len(list_of_item):
                list_of_item.pop(0)
            t.add_row(list(list_of_item))
            print(t)
        else:
            print(item)

    @staticmethod
    def show_items(items: list, type : TypeOfTable = TypeOfTable.NONE):
        print("Items:")
        if type != TypeOfTable.NONE:
            t = PrettyTable(list_of_fields[type])
            for item in items:
                list_of_item = item.get_data()
                if len(list_of_fields[type]) < len(list_of_item):
                    list_of_item.pop(0)
                t.add_row(list(list_of_item))
            print(t)
        else:
            for item in items:
                print(item)


    @staticmethod
    def show_error(err: str):
        print(f"Error: {err}")

    @staticmethod
    def show_text(text: str):
        print(text)





