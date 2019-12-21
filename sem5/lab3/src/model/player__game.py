from sqlalchemy import Column, Integer, Text, ForeignKey
from model.model_config import Base


class Player__Game(Base):
    __tablename__ = 'player__game'

    def __init__(self, game_id: int, player_id: int):
        self.game_id = game_id
        self.player_id = player_id

    game_id = Column(Integer, ForeignKey('developer_company.id', onupdate='restrict', ondelete='restrict'),
                     primary_key=True, nullable=False, autoincrement=False)
    player_id = Column(Text, ForeignKey('developer_company.id', onupdate='restrict', ondelete='restrict'),
                       primary_key=True, nullable=False, autoincrement=False)

    def get_data(self):
        return self.game_id, self.player_id

    def __str__(self):
        return f"Player__Game [game_id={self.game_id}, player_id={self.player_id}] "

    @staticmethod
    def create_obj(fields_list: dict):
        return Player__Game(**fields_list)
