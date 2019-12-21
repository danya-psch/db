from sqlalchemy import Column, Integer, Text, Date
from model.model_config import Base


class Player(Base):
    __tablename__ = 'player'

    def __init__(self, nickname: str, ip: str, date_of_birth: Date, id: int = None):
        self.id = id
        self.nickname = nickname
        self.ip = ip
        self.date_of_birth = date_of_birth

    # def __init__(self, id: int, nickname: str, ip: str, date_of_birth: Date):
    #     self.id = id
    #     self.nickname = nickname
    #     self.ip = ip
    #     self.date_of_birth = date_of_birth

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
