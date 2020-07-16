import configparser

import psycopg2 as psycopg2
import mysql.connector
from mysql.connector import Error


class PostgresDB:

    def get_connection(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        connection = psycopg2.connect(
            user=config['Postgres-configdb']['user'],
            password=config['Postgres-configdb']['password'],
            host=config['Postgres-configdb']['host'],
            port=config['Postgres-configdb']['port'],
            database=config['Postgres-configdb']['database'])
        return connection

    def get_connection_afiniti(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        connection = psycopg2.connect(
            user=config['Postgres-afinitidb']['user'],
            password=config['Postgres-afinitidb']['password'],
            host=config['Postgres-afinitidb']['host'],
            port=config['Postgres-afinitidb']['port'],
            database=config['Postgres-afinitidb']['database'])
        return connection

    def close_connection(self, connection):
        connection.close()


class MySQLDB1:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.host = config['mysql']['host']
        self.database = config['mysql']['name']
        self.user = config['mysql']['user']
        self.password = config['mysql']['pwd']

    def get_connection(self):
        print(self.host)
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database,
            auth_plugin='mysql_native_password'
        )
        return connection

    def close_connection(self, connection):
        connection.close()

    def get_cursor(self):
        return self.db.cursor()

    def select(self, query):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        result = cursor.fetchall()
        self.close_connection(connection)
        return result

    def insert(self, query):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.commit(query)

    def delete(self, query):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.commit(query)
        self.close_connection(connection)
