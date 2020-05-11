from controller.AdminController import AdminController
from controller.Controller import Controller
from controller.EmulationController import EmulationController
from controller.UserController import UserController
from servers.neo4j_server.Neo4jServer import Neo4jServer
from view import View
from faker import Faker
import random


def emulation():

    fake = Faker()
    users_count = 5
    users = [fake.profile(fields=['username'], sex=None)['username'] for u in range(users_count)]
    threads = []
    try:

        for i in range(users_count):
            threads.append(EmulationController(users[i], users, users_count, random.randint(1, 3)))
        for thread in threads:
            thread.start()

        AdminController()

    except Exception as e:
        View.show_error(str(e))
    finally:
        for thread in threads:
            if thread.is_alive():
                thread.stop()


if __name__ == "__main__":
    neo4j = Neo4jServer()
    neo4j.create_message(1, 2, {"id": 1, "tags": ["work"]})
    choice = Controller.make_choice(["Main", "Emulation"], "Program mode")
    if choice == 0:
        UserController()
    elif choice == 1:
        emulation()
