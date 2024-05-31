import psycopg2
import os
from psycopg2 import pool
from utils.utils import Config
from log.log import logger
from datetime import datetime

DATABASE_URL = os.environ['DATABASE_URL']


class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = Database.get_connection()
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


class Database:
    __connection_pool = None

    @staticmethod
    def initialise():
        Database.__connection_pool = psycopg2.connect(DATABASE_URL)
        Database.create_tables()
        logger.info(f'Database connection pool initialized')

    @staticmethod
    def get_connection():
        logger.info('Getting the database connection')
        return Database.__connection_pool

    @staticmethod
    def return_connection(connection):
        logger.info('Returning a connection to the pool')
        Database.__connection_pool.putconn(connection)
                
    @staticmethod
    def close_connections():
        logger.info('All connections in the pool have been closed')
        Database.__connection_pool.close()

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
            image_url TEXT NULL,
            FOREIGN KEY(topico_id) REFERENCES topicos(id))""")
            logger.info('Solutions table created')

            # Create versoes_sis_gestor table
            cursor.execute("""CREATE TABLE IF NOT EXISTS versoes_sis_gestor(
            id SERIAL PRIMARY KEY,
            versao TEXT NOT NULL UNIQUE )""")
            logger.info('Versoes_sis table created')

            # Create versoes_sis_pdv table
            cursor.execute("""CREATE TABLE IF NOT EXISTS versoes_sis_pdv(
            id SERIAL PRIMARY KEY,
            versao TEXT NOT NULL UNIQUE )""")
            logger.info('Versoes_sis_pdv table created')

            # Create clientes table
            cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            versao_sis_id_gestor INTEGER NULL,
            versao_sis_id_pdv INTEGER NULL,
            last_change_at TIMESTAMP,
            FOREIGN KEY (versao_sis_id_gestor) REFERENCES versoes_sis_gestor(id),
            FOREIGN KEY (versao_sis_id_pdv) REFERENCES versoes_sis_gestor(id))""")
            logger.info('Clientes table created')

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
                logger.error(f'Failed to search solution with "{search_term}" term(s) and {topic_id} topic ID. '
                             f'Erro: {e}')
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


    @staticmethod
    def add_version_gestor(version: str):
        with DatabaseConnection() as cursor:
            try:
                cursor.execute('INSERT INTO versoes_sis_gestor(versao)'
                               'VALUES (%s)', (version,))
                logger.info(f'Version "{version}" create in version_sis_gestor successfully')
                return True
            except Exception as e:
                logger.error(f'Failed to add version {version} in version_sis_gestor. Erro: {e}')
                return False

    @staticmethod
    def add_version_pdv(version: str):
        with DatabaseConnection() as cursor:
            try:
                cursor.execute('INSERT INTO versoes_sis_pdv(versao)'
                               'VALUES (%s)', (version,))
                logger.info(f'Version "{version}" create in version_sis_pdv successfully')
                return True
            except Exception as e:
                logger.error(f'Failed to add version {version} in version_sis_pdv. Erro: {e}')
                return False

    @staticmethod
    def get_versions_gestor():
        with DatabaseConnection() as cursor:
            try:
                cursor.execute('SELECT * FROM versoes_sis_gestor')
                logger.info(f'Successfully getting all the solution from version_sis_gestor')
                return cursor.fetchall()
            except Exception as e:
                logger.error(f'Failed to get all the versions from version_sis_gestor. Erro: {e}')
                return None

    @staticmethod
    def get_versions_pdv():
        with DatabaseConnection() as cursor:
            try:
                cursor.execute('SELECT * FROM versoes_sis_pdv')
                logger.info(f'Successfully getting all the versions from version_sis_pdv')
                return cursor.fetchall()
            except Exception as e:
                logger.error(f'Failed to get all the versions from version_sis_pdv. Erro: {e}')
                return None

    @staticmethod
    def add_cliente(name: str, version_gestor_id: int, version_pdv_id: int):
        with DatabaseConnection() as cursor:
            try:
                time_now = datetime.now()

                cursor.execute('INSERT INTO clientes(name, versao_sis_gestor_id, versao_sis_pdv_id, last_change_at)'
                               'VALUES (%s, %s, %s, %s)', (name, version_gestor_id, version_pdv_id, time_now))
                logger.info(f'Cliente {name} successfully created at cliente table')
                return True
            except Exception as e:
                logger.error(f'Failed to create cliente {name}. Erro: {e}')
                return False


def has_the_comma(url_string):
    # Find the ',' in a url_string
    for character in url_string:
        if character == ',':
            return True
    return False


def replace_the_comma(url_string):
    has_comma = has_the_comma(url_string)
    if has_comma:
        return url_string.replace(',', ';')
    else:
        return url_string
