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

    # def __init__(self, id: int, name: str, salary: int, experience: float, developer_company_id: int, date_of_birth: Date):
    #     self.id = id
    #     self.name = name
    #     self.salary = salary
    #     self.experience = experience
    #     self.developer_company_id = developer_company_id
    #     self.date_of_birth = date_of_birth

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
