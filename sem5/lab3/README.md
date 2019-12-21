Лабораторна робота No 3. Ознайомлення з базовими операціями СУБД PostgreSQL
=====================

Варіант завдання
-----------------------------------
15 варінт згідно номема у списку

| Види індексів | Умови для тригера |
|-------------|-----------|
| Hash, BRIN | before delete, update |

Опис структури бази даних
-----------------------------------


| Відношення  | Атрибути  |
|-------------|-----------|
| Відношення "developer_company " <br> Вміщує інформацію про компанію розробника|   id - ідентифікатор компанії(integer)<br>name – унікальна назва компанії(text)<br>date_of_birth – дата створення коппанії(date)|
| Відношення "game__player" <br> Вміщує інформацію про відношення гравця до ігор|   id - ідентифікатор гравця(integer)<br>, game_id – ідентифікатор гри(text)|
| Відношення "developer_company__game" <br> Вміщує інформацію про відношення компанії розробника до ігор, які були нею розроблені| developer_company_id - ідентифікатор компанії(integer)<br>game_id - ідентифікатор гри(integer)<br>release_date - дата випуску гри(date)|
| Відношення "game "<br>Вміщує інформацію про гру що розробляється компанією |  id - ідентифікатор гри(integer)<br>age_restrictions – містить інформацію про вікові обмеження гри(int) <br>name – унікальна назва гри(text) <br>genre – жанр гри(text)|
| Відношення " player " <br>Вміщує інформацію про гравця, що грає в гру |  id - ідентифікатор гравця(integer)<br>date_of_birth – дата народження гравця(date)<br>nickname – ім’я, яке гравець використовує у грі(text)<br> IP – унікальний ідентифікатор, який використовується для адресації комп’ютера в мережі(text)|
| Відношення " programmer "<br>Вміщує інформацію про програміста, який працює в компанії  |  id - ідентифікатор програміста(integer)<br>date_of_birth – дата народження програміста(date) <br>full_name – повне ім’я програміста(text) <br>salary – заробітна плата програміста(int) <br>experience – досвід роботі програміста в роках(real) <br>company – назва компанії в якій працює програміст(text)|
|Відношення "dead_programmers"<br>Вміщує інформацію про мертвих програмістів | id - ідентифікатор програміста(integer)<br> name - ім’я програміста(text) <br>|


Завдання №1: оновлений програмний код
=====================
```
model/__init__.py
```

```python
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
```

```
model/developer_company.py
```

```python
from sqlalchemy import Column, Integer, Text, Date
from model.model_config import Base


class DeveloperCompany(Base):
    __tablename__ = 'developer_company'

    def __init__(self, name: str, date_of_creation: Date, description: str, id: int = None):
        self.id = id
        self.name = name
        self.date_of_creation = date_of_creation
        self.description = description

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    date_of_creation = Column(Date, nullable=False)
    description = Column(Text, nullable=False)

    def get_data(self):
        return self.id, self.name, self.date_of_creation, self.description

    def __str__(self):
        return f"DeveloperCompany [id={self.id}, name={self.name}, date_of_creation={self.date_of_creation}, " \
               f"description={self.description}] "

    @staticmethod
    def create_obj(fields_list: dict):
        return DeveloperCompany(**fields_list)

```

```
model/game.py
```

```python
from sqlalchemy import Column, Integer, Text
from model.model_config import Base


class Game(Base):
    __tablename__ = 'game'

    def __init__(self, name: str, genre: str, age_restrictions: int, id: int = None):
        self.id = id
        self.name = name
        self.genre = genre
        self.age_restrictions = age_restrictions

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    genre = Column(Text, nullable=False)
    age_restrictions = Column(Integer, nullable=False)

    def get_data(self):
        return self.id, self.name, self.genre, self.age_restrictions

    def __str__(self):
        return f"Game [id={self.id}, name={self.name}, genre={self.genre}, age_restrictions={self.age_restrictions}]"

    @staticmethod
    def create_obj(fields_list: dict):
        return Game(**fields_list)

```

```
model/player.py
```

```python
from sqlalchemy import Column, Integer, Text, Date
from model.model_config import Base


class Player(Base):
    __tablename__ = 'player'

    def __init__(self, nickname: str, ip: str, date_of_birth: Date, id: int = None):
        self.id = id
        self.nickname = nickname
        self.ip = ip
        self.date_of_birth = date_of_birth

    id = Column(Integer, primary_key=True)
    nickname = Column(Text, nullable=False)
    ip = Column(Text, nullable=False)
    date_of_birth = Column(Date, nullable=False)

    def get_data(self):
        return self.id, self.nickname, self.ip, self.date_of_birth

    def __str__(self):
        return f"Player [id={self.id}, nickname={self.nickname}, ip={self.ip}, age_restrictions={self.date_of_birth}]"

    @staticmethod
    def create_obj(fields_list: dict):
        return Player(**fields_list)

```

```
model/programmer.py
```

```python
from sqlalchemy import ForeignKey, Column, Integer, Text, Date, Float
from model.model_config import Base


class Programmer(Base):
    __tablename__ = 'programmer'

    def __init__(self, name: str, salary: int, experience: float, developer_company_id: int, date_of_birth: Date, id: int = None):
        self.id = id
        self.name = name
        self.salary = salary
        self.experience = experience
        self.developer_company_id = developer_company_id
        self.date_of_birth = date_of_birth

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    salary = Column(Integer, nullable=False)
    experience = Column(Float, nullable=False)
    developer_company_id = Column(Integer, ForeignKey('developer_company.id', onupdate='restrict', ondelete='restrict'), nullable=False)
    date_of_birth = Column(Date, nullable=False)

    def get_data(self):
        return self.id, self.name, self.salary, self.experience, self.developer_company_id, self.date_of_birth

    def __str__(self):
        return f"Player [id={self.id}, name={self.name}, salary={self.salary}, experience={self.experience}, " \
               f"developer_company_id={self.developer_company_id}, date_of_birth={self.date_of_birth}] "

    @staticmethod
    def create_obj(fields_list: dict):
        return Programmer(**fields_list)

```
Завдання №2: команди створення індексів, тексти і час виконання запитів SQL
=====================
Команди SQL створення індексів
SQL запити
Завдання №3: команди, що ініціюють виконання тригера, текст тригера та скріншоти зі змінами у таблицях бази даних
=====================

Завдання №4: скріншоти з ходом виконання запитів та їх результатів у обох транзакціях по кожному рівню ізоляції
=====================
READ COMMITTED
-----------------------------------

| Transction #1 | Transction #2 |
|---------------|---------------|
| ![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/READ_COMMITTED_1.png)| ![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/READ_COMMITTED_2.png)|
-----------------------------------

| Transction #1                                                                    | Transction #2 |
|----------------------------------------------------------------------------------|---------------|
|![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/READ_COMMITTED_3.png)|               |
|               |![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/READ_COMMITTED_4.png)|
|![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/READ_COMMITTED_5.png)|               |
|               |![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/READ_COMMITTED_6.png)|
|![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/READ_COMMITTED_7.png)|               |
-----------------------------------

REPEATABLE READ
-----------------------------------

| Transction #1 | Transction #2 |
|---------------|---------------|
| ![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/REPEATABLE_READ_1.png)| ![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/REPEATABLE_READ_2.png)|
-----------------------------------

| Transction #1                                                                     | Transction #2 |
|-----------------------------------------------------------------------------------|---------------|
|![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/REPEATABLE_READ_3.png)|               |
|               |![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/REPEATABLE_READ_4.png)|
|![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/REPEATABLE_READ_5.png)|               |
|               |![](https://github.com/DanyaPes/db/blob/master/sem5/lab3/img/REPEATABLE_READ_6.png)|
