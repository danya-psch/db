Лабораторна робота No 2. Практика використаннясервера Redis
=====================

Завдання
-----------------------------------
[Постановка завдання](http://scs.kpi.ua/sites/default/files/lab2_bd2-db2019_2020.pdf)

Лістинг коду
-----------------------------------
```
main.py
```

```python
def main():
    fake = Faker()
    users_count = 5
    r = redis.Redis()
    r.flushall()
    users = [fake.profile(fields=['username'], sex=None)['username'] for u in range(users_count)]
    threads = []
    try:

        for i in range(users_count):
            threads.append(EmulationController(users[i], users, users_count, random.randint(100, 5000)))
        for thread in threads:
            thread.start()

        workers_count = 5
        workers = []
        for x in range(workers_count):
            worker = Worker(random.randint(0, 3))
            workers.append(worker)
            worker.start()

        UserController()

        for thread in threads:
            if thread.is_alive():
                thread.stop()
        for worker in workers:
            worker.stop()

        print("\nEND")
    except Exception as e:
        View.show_error(str(e))


if __name__ == "__main__":
    main()
```


```
RedisServer.py
```

```python
logging.basicConfig(filename="./events.log", level=logging.INFO, filemode='w')


class RedisServer(object):
    def __init__(self):
        self.__r = redis.Redis(charset="utf-8", decode_responses=True)

    def registration(self, username, role):
        if self.__r.hget('users:', username):
            raise Exception(f"User with name: \'{username}\' already exists")

        if role != 'utilizer' and role != 'admin':
            raise Exception("There is not rule like that. Enter one of the following: utilizer, admin")

        user_id = self.__r.incr('user:id:')
        pipeline = self.__r.pipeline(True)
        pipeline.hset('users:', username, user_id)
        pipeline.hmset(f"user:{user_id}", {
            'login': username,
            'id': user_id,
            'queue': 0,
            'checking': 0,
            'blocked': 0,
            'sent': 0,
            'delivered': 0,
            'role': role
        })

        pipeline.execute()
        logging.info(f"User {username} registered at {datetime.datetime.now()} \n")
        return user_id

    def sign_in(self, username):
        user_id = self.__r.hget("users:", username)

        if not user_id:
            raise Exception(f"User {username} does not exist ")

        self.__r.sadd("online:", username)
        logging.info(f"User {username} logged in at {datetime.datetime.now()} \n")
        return {'user_id': int(user_id), 'role': self.__r.hget(f"user:{int(user_id)}", 'role')}

    def sign_out(self, user_id) -> int:
        logging.info(f"User {user_id} signed out at {datetime.datetime.now()} \n")
        return self.__r.srem("online:", self.__r.hmget(f"user:{user_id}", 'login')[0])

    def create_message(self, message_text, consumer, sender_id) -> int:

        message_id = int(self.__r.incr('message:id:'))
        consumer_id = self.__r.hget("users:", consumer)

        if not consumer_id:
            raise Exception(f"{consumer} user does not exist, user can't send a message")

        pipeline = self.__r.pipeline(True)

        pipeline.hmset('message:%s' % message_id, {
            'text': message_text,
            'id': message_id,
            'sender_id': sender_id,
            'consumer_id': consumer_id,
            'status': "created"
        })
        pipeline.lpush("queue:", message_id)
        pipeline.hmset('message:%s' % message_id, {
            'status': 'queue'
        })
        pipeline.zincrby("sent:", 1, "user:%s" % self.__r.hmget(f"user:{sender_id}", 'login')[0])
        pipeline.hincrby(f"user:{sender_id}", "queue", 1)
        pipeline.execute()

        return message_id

    def get_messages(self, user_id):
        messages = self.__r.smembers(f"sentto:{user_id}")
        messages_list = []
        for message_id in messages:
            message = self.__r.hmget(f"message:{message_id}", ["sender_id", "text", "status"])
            sender_id = message[0]
            messages_list.append("From: %s - %s" % (self.__r.hmget("user:%s" % sender_id, 'login')[0], message[1]))
            if message[2] != "delivered":
                pipeline = self.__r.pipeline(True)
                pipeline.hset(f"message:{message_id}", "status", "delivered")
                pipeline.hincrby(f"user:{sender_id}", "sent", -1)
                pipeline.hincrby(f"user:{sender_id}", "delivered", 1)
                pipeline.execute()
        return messages_list

    def get_message_statistics(self, user_id):
        current_user = self.__r.hmget(f"user:{user_id}", ['queue', 'checking', 'blocked', 'sent', 'delivered'])
        return "In queue: %s\nChecking: %s\nBlocked: %s\nSent: %s\nDelivered: %s" % tuple(current_user)

    def get_online_users(self) -> list:
        return self.__r.smembers("online:")

    def get_top_senders(self, amount_of_top_senders) -> list:
        return self.__r.zrange("sent:", 0, int(amount_of_top_senders) - 1, desc=True, withscores=True)

    def get_top_spamers(self, amount_of_top_spamers) -> list:
        return self.__r.zrange("spam:", 0, int(amount_of_top_spamers) - 1, desc=True, withscores=True)

```

```
Worker.py
```

```python
class Worker(Thread):

    def __init__(self, delay):
        Thread.__init__(self)
        self.__loop = True
        self.__r = redis.Redis(charset="utf-8", decode_responses=True)
        self.__delay = delay

    def run(self):
        while self.__loop:
            message = self.__r.brpop("queue:")
            if message:
                message_id = int(message[1])

                self.__r.hmset(f"message:{message_id}", {
                    'status': 'checking'
                })
                message = self.__r.hmget(f"message:{message_id}", ["sender_id", "consumer_id"])
                sender_id = int(message[0])
                consumer_id = int(message[1])
                self.__r.hincrby(f"user:{sender_id}", "queue", -1)
                self.__r.hincrby(f"user:{sender_id}", "checking", 1)
                time.sleep(self.__delay)
                is_spam = random.random() > 0.6
                pipeline = self.__r.pipeline(True)
                pipeline.hincrby(f"user:{sender_id}", "checking", -1)
                if is_spam:
                    sender_username = self.__r.hmget(f"user:{sender_id}", 'login')[0]
                    pipeline.zincrby("spam:", 1, f"user:{sender_username}")
                    pipeline.hmset(f"message:{message_id}", {
                        'status': 'blocked'
                    })
                    pipeline.hincrby(f"user:{sender_id}", "blocked", 1)
                    pipeline.publish('spam', f"User {sender_username} sent spam message: \"%s\"" %
                                     self.__r.hmget("message:%s" % message_id, ["text"])[0])
                else:
                    pipeline.hmset(f"message:{message_id}", {
                        'status': 'sent'
                    })
                    pipeline.hincrby(f"user:{sender_id}", "sent", 1)
                    pipeline.sadd(f"sentto:{consumer_id}", message_id)
                pipeline.execute()

    def stop(self):
        self.__loop = False

```

```
EmulationController.py
```

```python
fake = Faker()


class EmulationController(Thread):
    def __init__(self, username, users_list, users_count, loop_count):
        Thread.__init__(self)
        self.__loop_count = loop_count
        self.__server = RedisServer()
        self.__users_list = users_list
        self.__users_count = users_count
        self.__server.registration(username, "utilizer")
        self.__user_id = self.__server.sign_in(username)['user_id']

    def run(self):
        while self.__loop_count > 0:
            message_text = fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)
            receiver = self.__users_list[randint(0, self.__users_count - 1)]
            self.__server.create_message(message_text, receiver, self.__user_id)
            self.__loop_count -= 1

        self.stop()

    def stop(self):
        self.__server.sign_out(self.__user_id)
        self.__loop_count = 0
```

```
UserController.py
```

```python
class UserController(object):
    def __init__(self):
        self.__server = RedisServer()
        self.__menu = 'Main menu'
        self.__current_user_id = -1
        self.__loop = True
        atexit.register(self.sign_out, self)
        self.start()

    def start(self):
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
    def stop_loop(controller):
        controller.__loop = False

    @staticmethod
    def get_func_arguments(func, amount_of_missing_arguments=0) -> list:
        from data import special_parameters
        list_of_parameters = signature(func).parameters
        list_of_arguments = []
        length = len(list_of_parameters)
        for i in range(length - amount_of_missing_arguments):
            list_of_arguments.append(UserController.get_value(
                f"Enter {list(list_of_parameters)[i]}{ special_parameters[list(list_of_parameters)[i]] if list(list_of_parameters)[i] in special_parameters else '' }: ", str))
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
```


```
data.py
```

```python
from controller.UserController import UserController

menu_list = {
    'Main menu': {
        'Registration': UserController.registration,
        'Sign in': UserController.sign_in,
        'Exit': UserController.stop_loop,
    },
    'Utilizer menu': {
        'Sign out': UserController.sign_out,
        'Send a message': UserController.send_message,
        'Inbox messages': UserController.inbox_message,
        'My messages statistics': UserController.get_message_statistics,
    },
    'Admin menu': {
        'Sign out': UserController.sign_out,
        'Online users': UserController.get_online_users,
        'Top senders': UserController.get_top_senders,
        'Top spamers': UserController.get_top_spamers,
    }
}

roles = {
    'utilizer': 'Utilizer menu',
    'admin': 'Admin menu'
}

special_parameters = {
    'role': '(admin or utilizer)'
}
```

```
view/__init__.py
```

```python
class View(object):

    @staticmethod
    def draw_menu(menu_list, name_of_menu: str):
        print(f"\n{name_of_menu}")
        number = 0
        for menu_item in menu_list:
            print(f" {number}: {menu_item}")
            number += 1

    @staticmethod
    def show_item(item):
        print(f"Item: {item}")

    @staticmethod
    def show_items(items: list):
        count = 1
        for item in items:
            print(f"{count}: {item}")
            count += 1

    @staticmethod
    def show_error(err: str):
        print(f"Error: {err}")

    @staticmethod
    def show_text(text: str):
        print(text)

    @staticmethod
    def print_line():
        print('-----------------------------------------------------------------------------------------')

    @staticmethod
    def print_list(name_of_list, list):
        print(name_of_list)
        count = 1
        for item in list:
            print(f"{count}: {item}")
            count += 1
```

Лістинг згенерованих файлів
-----------------------------------
```
events.log
```

```log
INFO:root:User steven66 registered at 2020-04-09 18:09:20.454372 

INFO:root:User steven66 logged in at 2020-04-09 18:09:20.454800 

INFO:root:User thomascrystal registered at 2020-04-09 18:09:20.456092 

INFO:root:User thomascrystal logged in at 2020-04-09 18:09:20.456574 

INFO:root:User michael93 registered at 2020-04-09 18:09:20.457816 

INFO:root:User michael93 logged in at 2020-04-09 18:09:20.458110 

INFO:root:User michael48 registered at 2020-04-09 18:09:20.459246 

INFO:root:User michael48 logged in at 2020-04-09 18:09:20.459515 

INFO:root:User chamberssusan registered at 2020-04-09 18:09:20.460553 

INFO:root:User chamberssusan logged in at 2020-04-09 18:09:20.460821 

INFO:root:User admin registered at 2020-04-09 18:09:26.203206 

INFO:root:User admin logged in at 2020-04-09 18:09:28.366059 

INFO:root:User 6 signed out at 2020-04-09 18:09:48.158241 

INFO:root:User 1 signed out at 2020-04-09 18:09:50.505600 

INFO:root:User 2 signed out at 2020-04-09 18:09:50.524044 

INFO:root:User 3 signed out at 2020-04-09 18:09:50.537189 

INFO:root:User 4 signed out at 2020-04-09 18:09:50.546448 

INFO:root:User 5 signed out at 2020-04-09 18:09:50.553150 

INFO:root:User michael48 logged in at 2020-04-09 18:10:05.735256 

INFO:root:User 4 signed out at 2020-04-09 18:10:23.555879 
```

Приклади роботи програми
-----------------------------------
Main menu
-----------------------------------
![](https://github.com/danya-psch/db/blob/master/sem6/lab2/img/main_menu.png)
-----------------------------------
Online users
-----------------------------------
![](https://github.com/danya-psch/db/blob/master/sem6/lab2/img/online_users.png)
-----------------------------------
Inbox messages
-----------------------------------
![](https://github.com/danya-psch/db/blob/master/sem6/lab2/img/inbox_messages.png)
-----------------------------------
Message statistics
-----------------------------------
![](https://github.com/danya-psch/db/blob/master/sem6/lab2/img/message_statistics.png)
-----------------------------------
Message sending
-----------------------------------
![](https://github.com/danya-psch/db/blob/master/sem6/lab2/img/send_a_message.png)
-----------------------------------
Top senders
-----------------------------------
![](https://github.com/danya-psch/db/blob/master/sem6/lab2/img/top_senders.png)
-----------------------------------
Top spamers
-----------------------------------
![](https://github.com/danya-psch/db/blob/master/sem6/lab2/img/top_spamers.png)

