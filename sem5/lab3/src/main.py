from config import config
from controller.main_controller import MainController
import logging


def setup_db_logging():
    handler_sql = logging.FileHandler('db.log')
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.INFO)
    sql_logger.addHandler(handler_sql)
    sql_logger.propagate = False


if __name__ == '__main__':
    setup_db_logging()
    main_controller = MainController(**config)
    main_controller.start()
    main_controller.close()
