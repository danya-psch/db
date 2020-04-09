from random import randint
from threading import Thread, Event
from redis_server.RedisServer import RedisServer
from faker import Faker

fake = Faker()


class EmulationController(Thread):
    def __init__(self, username, users_list, users_count):
        Thread.__init__(self)
        self.__stop_event = Event()
        self.__server = RedisServer()
        self.__users_list = users_list
        self.__users_count = users_count
        self.__server.registration(username, "utilizer")
        self.__user_id = self.__server.sign_in(username)['user_id']

    def run(self):
        while True:
            message_text = fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)
            receiver = self.__users_list[randint(0, self.__users_count - 1)]
            self.__server.create_message(message_text, receiver, self.__user_id)

    def stop(self):
        self.__server.sign_out(self.__user_id)
        self.__stop_event.set()
