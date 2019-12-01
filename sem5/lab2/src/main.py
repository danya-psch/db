'''import psycopg2

connection = psycopg2.connect(host="localhost", port="5432", database="db_lab1", user="postgres", password="reRhsybrcs1038")
cursor = connection.cursor()
cursor.execute("SELECT * FROM game")
row = cursor.fetchone()

while row is not None:
	print(row)
	row = cursor.fetchone()

'''
import psycopg2
from config import config
from controller.main_controller import MainController


if __name__ == '__main__':
	connection = psycopg2.connect(**config)
	main_controller = MainController(connection)
	main_controller.start()
	main_controller.close()
