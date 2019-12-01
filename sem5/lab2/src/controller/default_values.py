default_games = [
    {
        'id': 1,
        'name': '\'Dark Souls III\'',
        'genre': '\'Action role-playing\'',
        'age_restrictions': 16,
    },
    {
        'id': 2,
        'name': '\'Bloodborne\'',
        'genre': '\'Action role-playing\'',
        'age_restrictions': 16,
    },
]
default_players = [
    {
        'id': 1,
        'nickname': '\'Vlad\'',
        'ip': '\'192.168.5.1\'',
        'date_of_birth': '\'2005-05-30\''
    },
    {
        'id': 2,
        'nickname': '\'Danya\'',
        'ip': '\'192.168.5.2\'',
        'date_of_birth': '\'2007-08-31\''
    },
]
default_developer_companies = [
    {
        'id': 1,
        'name': '\'FromSoftware\'',
        'date_of_creation': '\'1986-11-01\'',
        'description': '\'FromSoftware, Inc. is a Japanese video game development company founded in November 1986. '
                       'The company is known primarily outside Japan for being the developers of the Armored Core and '
                       'Souls series, as well as Bloodborne and Sekiro: Shadows Die Twice. \'',
    },
    {
        'id': 2,
        'name': '\'4AGames\'',
        'date_of_creation': '\'1998-11-01\'',
        'description': '\'4A Games Limited is a Ukrainian-Maltese video game developer based in Sliema, Malta. The '
                       'company was founded in Kiev, Ukraine, in 2006 by three developers who departed from GSC Game '
                       'World. In 2014, 4A Games moved its headquarters to Sliema, wherein the Kiev office was '
                       'retained as a sub-studio. The company is best known for developing the Metro game series. \'',
    },
]
default_programmers = [
    {
        'id': 1,
        'name': '\'Danya\'',
        'salary': 500,
        'experience': 0.5,
        '___developer_company_id': 2,
        'date_of_birth': '\'2000-08-31\'',
    },
    {
        'id': 2,
        'name': '\'Vlad\'',
        'salary': 600,
        'experience': 0.5,
        '___developer_company_id': 1,
        'date_of_birth': '\'1998-05-30\'',
    },
    {
        'id': 3,
        'name': '\'Yaroslav\'',
        'salary': 700,
        'experience': 0.5,
        '___developer_company_id': 1,
        'date_of_birth': '\'1996-08-20\'',
    },
]
default_developer_company__game = [
    {
        'developer_company_id': 1,
        'game_id': 1,
        'release_date': '\'2016-04-12\''
    },
    {
        'developer_company_id': 1,
        'game_id': 2,
        'release_date': '\'2015-03-24\''
    }
]
default_player__game = [
    {
        '___game_id': 1,
        '___player_id': 1,
    },
    {
        '___game_id': 1,
        '___player_id': 2,
    },
    {
        '___game_id': 2,
        '___player_id': 1,
    },
    {
        '___game_id': 2,
        '___player_id': 2,
    },
]

