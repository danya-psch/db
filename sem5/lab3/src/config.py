import os

config = {
    'dialect': 'postgresql',
    'host': "localhost",
    'port': "5432",
    'db_name': "db_lab1",
    'user': "postgres",
    'password': "reRhsybrcs1038",
}
'''
config = {
    '': 'postgresql',
    'host': "localhost",
    'port': "5432",
    'db_name': "db_lab1",
    'user': "postgres",
    'password': "reRhsybrcs1038"
    
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'db_name': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
}
'''
