import psycopg2
import os
from psycopg2 import pool
from utils.utils import Config
from log.log import logger
from datetime import datetime


class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self.conn = Database.get_connection(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        logger.info('Database connection opened.')
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.conn.rollback()
            logger.error('Transaction rolled back due to a error: %e', exc_val)
        else:
            self.cursor.close()
            self.conn.commit()
            logger.info('Transaction committed')
        Database.return_connection(self.conn)


class Database:
    __connection_pool = None

    @staticmethod
    def initialise():
        config_data = Config.get_config()
        Database.__connection_pool = pool.SimpleConnectionPool(20,
                                                               10,
                                                               user=config_data['DB_USER'],
                                                               password=config_data['DB_PASSWORD'],
                                                               database=config_data['DB_NAME'],
                                                               host=config_data['DB_HOST'])
        Database.create_tables()
        logger.info(f'Database connection pool initialized (Database: {config_data['DB_NAME']})')

    @staticmethod
    def get_connection():
        logger.info('Getting a connection from the pool')
        return Database.__connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        logger.info('Returning a connection to the pool')
        Database.__connection_pool.putconn(connection)
                
    @staticmethod
    def close_all_connections():
        logger.info('All connections in the pool have been closed')
        Database.__connection_pool.closeall()

    @staticmethod
    def create_tables():
        with DatabaseConnection() as cursor:

            # Create topic table
            cursor.execute("""CREATE TABLE IF NOT EXISTS topicos (
            id SERIAL PRIMARY KEY,
            topic TEXT NOT NULL,
            descricao TEXT NULL,
            created_at TIMESTAMP)""")
            logger.info('Topics table created')

            # Create solutions table
            cursor.execute("""CREATE TABLE IF NOT EXISTS solucoes (
            id SERIAL PRIMARY KEY,
            topico_id INTEGER NOT NULL,
            titulo TEXT NOT NULL UNIQUE,
            solucao_desc TEXT NULL,
            created_at TIMESTAMP NOT NULL,
            modified_at TIMESTAMP NULL,
            image_url TEXT,
            FOREIGN KEY(topico_id) REFERENCES topicos(id))""")
            logger.info('Solutions table created')

    @staticmethod
    def set_topic(topic: str, topic_des: str = None) -> bool:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM topicos WHERE topic = %s", (topic,))
            time_now = datetime.now()
            existing_topic = cursor.fetchone()
            if existing_topic is not None:
                logger.error(f'Topic {topic} already exists')
                return False
            cursor.execute("INSERT INTO topicos (topic, descricao, created_at) VALUES (%s, %s, %s)",
                           (topic, topic_des, time_now))
            return True

    @staticmethod
    def search_topic(search_term: str):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM topicos WHERE topic LIKE %s", (f'%{search_term}%',))
            return cursor.fetchall()

    @staticmethod
    def edit_topic(topic_id: int, new_topic_name: str):
        with DatabaseConnection() as cursor:
            try:
                cursor.execute("UPDATE topicos SET topic = %s WHERE id = %s", (new_topic_name, topic_id))
                logger.info(f'Topic with ID {topic_id} successfully updated to {new_topic_name}')
                return True
            except Exception as e:
                logger.error(f'Failed to update topic with ID {topic_id}. Erro: {e}')
                return False

    @staticmethod
    def add_solution(topic_id: int, title: str, solution_desc: str, image_urls: str = None):
        with DatabaseConnection() as cursor:
            try:
                # Check if the image_urls string has comma into replace to ';'
                image_urls = replace_the_comma(image_urls)

                # Get the time for the timestamps datas
                time_now = datetime.now()

                cursor.execute("INSERT INTO solucoes(topico_id, titulo, solucao_desc, created_at, modified_at, "
                               "image_url) VALUES (%s, %s, %s, %s, %s, %s)",
                               (topic_id, title, solution_desc, time_now, time_now, image_urls))
                logger.info(f'Successfully add the solution {title} into topic ID {topic_id}.')
                return True
            except Exception as e:
                logger.error(f'Failed to add the solution {title} with topic ID {topic_id}; Error: {e}')
                return False

    @staticmethod
    def get_all_topics():
        with DatabaseConnection() as cursor:
            try:
                cursor.execute("SELECT * FROM topicos")
                logger.info(f'Successfully get all the topics names')
                return cursor.fetchall()
            except Exception as e:
                logger.error(f'Failed to get the topics names. Erro: {e}')
                return None

    @staticmethod
    def search_solution_by_title(topic_id: int, search_term: str):
        with DatabaseConnection() as cursor:
            try:
                cursor.execute('SELECT * FROM solucoes WHERE topico_id = %s AND titulo LIKE %s LIMIT 3',
                               (topic_id, f'%{search_term}%'))
                logger.info(f'Search for solution with the "{search_term}" term(s)')
                return cursor.fetchall()
            except Exception as e:
                logger.error(f'Failed to search solution with "{search_term}" term(s) and {topic_id} topic ID. Erro: {e}')
                return None

    @staticmethod
    def get_all_solutions_by_topic_id(topic_id: int):
        with DatabaseConnection() as cursor:
            try:
                cursor.execute('SELECT * FROM solucoes WHERE topico_id = %s', (topic_id,))
                logger.info(f'Getting all the solution with "{topic_id}" topic ID')
                return cursor.fetchall()
            except Exception as e:
                logger.error(f'Failed to get the solutions with {topic_id} topic ID. Erro: {e}')
                return None

    @staticmethod
    def get_solution_by_id(id: int):
        with DatabaseConnection() as cursor:
            try:
                cursor.execute('SELECT * FROM solucoes WHERE id = %s', (id,))
                logger.info(f'Getting all the solution with "{id}" topic ID')
                return cursor.fetchall()
            except Exception as e:
                logger.error(f'Failed to get the solutions with {id} topic ID. Erro: {e}')
                return None

    @staticmethod
    def edit_solution():
        pass

    @staticmethod
    def delete_solution():
        pass


def has_the_comma(url_string):
    # Find the ',' in a url_string
    for character in url_string:
        if character == ',':
            return True
    return False


def replace_the_comma(url_string):
    has_comma = has_the_comma(url_string)
    if has_comma:
        return url_string.replace(',',';')
    else:
        return url_string
