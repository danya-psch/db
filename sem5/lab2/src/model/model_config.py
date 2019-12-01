from datetime import date
from enum import Enum


class TypeOfTable(Enum):
    GAME = "game",
    PLAYER = "player",
    DEVELOPER_COMPANY = "developer_company",
    PROGRAMMER = "programmer",
    DEVELOPER_COMPANY__GAME = "developer_company__game",
    PLAYER__GAME = "player__game",


list_of_fields = {
    TypeOfTable.GAME: {
        'name': str,
        'genre': str,
        'age_restrictions': int,
    },
    TypeOfTable.PLAYER: {
        "nickname": str,
        "ip": str,
        "date_of_birth": date,
    },
    TypeOfTable.DEVELOPER_COMPANY: {
        'name': str,
        'date_of_creation': date,
        'description': str
    },
    TypeOfTable.PROGRAMMER: {
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
}

relation_field_to_table = {
    'developer_company_id': TypeOfTable.DEVELOPER_COMPANY,
    'game_id': TypeOfTable.GAME,
    'player_id': TypeOfTable.PLAYER,

}

relation_of_tables = {
    'developer_company__game': ['developer_company', 'game'],
    'player__game': ['player', 'game'],
    'programmer': ['developer_company'],
}