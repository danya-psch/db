from sqlalchemy import Column, Integer, Text, Date
from model.model_config import Base


class DeveloperCompany(Base):
    __tablename__ = 'developer_company'

    def __init__(self, name: str, date_of_creation: Date, description: str, id: int = None):
        self.id = id
        self.name = name
        self.date_of_creation = date_of_creation
        self.description = description

    # def __init__(self, id: int, name: str, date_of_creation: Date, description: str):
    #     self.id = id
    #     self.name = name
    #     self.date_of_creation = date_of_creation
    #     self.description = description

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

