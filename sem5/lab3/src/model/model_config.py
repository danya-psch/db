from datetime import date
from enum import Enum

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from model.game import Game
from model.player import Player
from model.developer_company import DeveloperCompany
from model.programmer import Programmer
from model.developer_company__game import DeveloperCompany__Game
from model.player__game import Player__Game


class TypeOfTable(Enum):
    GAME = "game",
    PLAYER = "player",
    DEVELOPER_COMPANY = "developer_company",
    PROGRAMMER = "programmer",
    DEVELOPER_COMPANY__GAME = "developer_company__game",
    PLAYER__GAME = "player__game",
    NONE = "none"


class_to_type_relation = {
    TypeOfTable.GAME: Game,
    TypeOfTable.PLAYER: Player,
    TypeOfTable.DEVELOPER_COMPANY: DeveloperCompany,
    TypeOfTable.PROGRAMMER: Programmer,
    TypeOfTable.DEVELOPER_COMPANY__GAME: DeveloperCompany__Game,
    TypeOfTable.PLAYER__GAME: Player__Game,
    TypeOfTable.NONE: None,
}


list_of_fields = {
    TypeOfTable.GAME: {
        'id': int,
        'name': str,
        'genre': str,
        'age_restrictions': int,
    },
    TypeOfTable.PLAYER: {
        'id': int,
        "nickname": str,
        "ip": str,
        "date_of_birth": date,
    },
    TypeOfTable.DEVELOPER_COMPANY: {
        'id': int,
        'name': str,
        'date_of_creation': date,
        'description': str
    },
    TypeOfTable.PROGRAMMER: {
        'id': int,
        'name': str,
        'salary': int,
        'experience': float,
        '___developer_company_id': int,
        'date_of_birth': date,
    },
    TypeOfTable.DEVELOPER_COMPANY__GAME: {
        '___developer_company_id': int,
        '___game_id': int,
        'release_date': date,
    },
    TypeOfTable.PLAYER__GAME: {
        '___game_id': int,
        '___player_id': int,
    },
    TypeOfTable.NONE: {
    },
}

relation_field_to_table = {
    'developer_company_id': TypeOfTable.DEVELOPER_COMPANY,
    'game_id': TypeOfTable.GAME,
    'player_id': TypeOfTable.PLAYER,

}

relation_of_tables = {
    TypeOfTable.DEVELOPER_COMPANY__GAME: ['developer_company', 'game'],
    TypeOfTable.PLAYER__GAME: ['player', 'game'],
    TypeOfTable.PROGRAMMER: ['developer_company'],
}

order_by = {
    TypeOfTable.DEVELOPER_COMPANY__GAME: 'game_id',
    TypeOfTable.PLAYER__GAME: 'game_id',
}


'''
relation_of_tables = {
    'developer_company__game': ['developer_company', 'game'],
    'player__game': ['player', 'game'],
    'programmer': ['developer_company'],
}
'''
