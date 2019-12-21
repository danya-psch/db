from sqlalchemy import Column, Integer, Text
from model.model_config import Base


class Game(Base):
    __tablename__ = 'game'

    def __init__(self, name: str, genre: str, age_restrictions: int, id: int = None):
        self.id = id
        self.name = name
        self.genre = genre
        self.age_restrictions = age_restrictions

    # def __init__(self, id: int, name: str, genre: str, age_restrictions: int):
    #     self.id = id
    #     self.name = name
    #     self.genre = genre
    #     self.age_restrictions = age_restrictions

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



