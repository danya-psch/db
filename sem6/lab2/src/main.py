from controller.UserController import UserController
from controller.EmulationController import EmulationController
from redis_server.Worker import Worker
from view import View
from faker import Faker
import random
import time


def main():
    fake = Faker()
    users_count = 5
    users = [fake.profile(fields=['username'], sex=None)['username'] for u in range(users_count)]
    threads = []
    try:

        for i in range(users_count):
            threads.append(EmulationController(users[i], users, users_count))
        for thread in threads:
            thread.start()

        workers_count = 5
        workers = []
        for x in range(workers_count):
            worker = Worker(random.randint(0, 3))
            workers.append(worker)
            worker.start()

        ucontroller = UserController()
        ucontroller.start()

        time.sleep(30)
        for thread in threads:
            thread.stop()
        for worker in workers:
            worker.stop()
        print("\nEND")
    except Exception as e:
        View.show_error(str(e))


if __name__ == "__main__":
    main()
