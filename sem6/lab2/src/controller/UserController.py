from inspect import signature
import atexit

from threading import Thread, Event
from view import View
from redis_server.RedisServer import RedisServer


class UserController(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__server = RedisServer()
        self.__menu = 'Main menu'
        self.__stop_event = Event()
        self.__current_user_id = -1
        self.__loop = True
        atexit.register(self.sign_out, self)
        # self.start()

    def run(self):
        from data import menu_list
        try:
            while self.__loop:
                choice = UserController.make_choice(menu_list[self.__menu].keys(), self.__menu)
                self.considering_choice(choice, list(menu_list[self.__menu].values()))
        except Exception as e:
            View.show_error(str(e))

    @staticmethod
    def make_choice(menu_list: list, name_of_menu: str):
        try:
            View.draw_menu(menu_list, name_of_menu)
            return UserController.get_uint_value("Make your choice: ", len(menu_list))

        except Exception as e:
            View.show_error(str(e))

    def considering_choice(self, choice: int, list_of_func: list):
        try:
            if choice > len(list_of_func) - 1:
                raise Exception("func is not exist")

            desired_func = list_of_func[choice]
            desired_func(self)
        except Exception as e:
            View.show_error(str(e))

    def stop(self):
        self.sign_out(self)
        self.__stop_event.set()

    @staticmethod
    def registration(controller):
        controller.__server.registration(*controller.get_func_arguments(controller.__server.registration))

    @staticmethod
    def sign_in(controller):
        pair = controller.__server.sign_in(*controller.get_func_arguments(controller.__server.sign_in))
        controller.__current_user_id = pair['user_id']
        from data import roles
        controller.__menu = roles[pair['role']]

    @staticmethod
    def sign_out(controller):
        if controller.__current_user_id != -1:
            controller.__server.sign_out(controller.__current_user_id)
            controller.__menu = 'Main menu'
            controller.__current_user_id = -1

    @staticmethod
    def send_message(controller):
        controller.__server.create_message(*controller.get_func_arguments(controller.__server.create_message, 1),
                                           controller.__current_user_id)

    @staticmethod
    def inbox_message(controller):
        messages = controller.__server.get_messages(controller.__current_user_id)
        View.print_list("Messages:", messages)

    @staticmethod
    def get_message_statistics(controller):
        statistics = controller.__server.get_message_statistics(controller.__current_user_id)
        View.show_item(statistics)

    @staticmethod
    def get_online_users(controller):
        online_users = controller.__server.get_online_users()
        View.print_list("Online users: ", online_users)

    @staticmethod
    def get_top_senders(controller):
        top_senders = controller.__server.get_top_senders(
            *controller.get_func_arguments(controller.__server.get_top_senders))
        View.print_list("Top senders: ", top_senders)

    @staticmethod
    def get_top_spamers(controller):
        top_spamers = controller.__server.get_top_spamers(
            *controller.get_func_arguments(controller.__server.get_top_spamers))
        View.print_list("Top spamers: ", top_spamers)

    @staticmethod
    def stop(controller):
        controller.__loop = False

    @staticmethod
    def get_func_arguments(func, amount_of_missing_arguments=0) -> list:
        list_of_parameters = signature(func).parameters
        list_of_arguments = []
        length = len(list_of_parameters)
        for i in range(length - amount_of_missing_arguments):
            list_of_arguments.append(UserController.get_value(f"Enter {list(list_of_parameters)[i]}: ", str))
        # for parameter in list_of_parameters:
        #     list_of_arguments.append(Controller.get_value(f"Enter {parameter}: ", str))
        return list_of_arguments

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
        while True:
            try:
                usr_input = input(msg)
                if type_of_var == str:
                    if len(usr_input) != 0:
                        return type_of_var(usr_input)
                else:
                    return type_of_var(usr_input)
            except Exception as e:
                View.show_error(str(e))
