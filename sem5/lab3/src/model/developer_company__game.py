from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from model.model_config import Base


class DeveloperCompany__Game(Base):
    __tablename__ = 'developer_company__game'

    def __init__(self, developer_company_id: int, game_id: int, release_date: Date):
        self.developer_company_id = developer_company_id
        self.game_id = game_id
        self.release_date = release_date

    developer_company_id = Column(Integer, ForeignKey('developer_company.id', onupdate='restrict', ondelete='restrict'),
                                  primary_key=True, nullable=False, autoincrement=False)
    game_id = Column(Text, ForeignKey('developer_company.id', onupdate='restrict', ondelete='restrict'),
                     primary_key=True, nullable=False, autoincrement=False)
    release_date = Column(Date, nullable=False)

    def get_data(self):
        return self.developer_company_id, self.game_id, self.release_date

    def __str__(self):
        return f"DeveloperCompany__Game [developer_company_id={self.developer_company_id}, game_id={self.game_id}, " \
               f"release_date={self.release_date}] "

    @staticmethod
    def create_obj(fields_list: dict):
        return DeveloperCompany__Game(**fields_list)
