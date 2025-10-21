import psycopg2
from psycopg2 import sql
from typing import List, Tuple, Optional
from src.models.company_and_vacancy_servise import Company, Vacancy
from config import config


class DBManager:
    """
    Класс для работы с PostgreSQL.
    """

    def __init__(self, filename="database.ini", section="postgresql"):
        params = config(filename, section)
        self._dsn = " ".join(f"{k}={v}" for k, v in params.items())
        self._conn = psycopg2.connect(**params)

    def connect(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(self._dsn)
        return self._conn

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()

    def create_tables(self):
        """
        Создание таблиц компаний и вакансий.
        Таблица вакансий имеет FK на таблицу компаний.
        """
        create_companies = """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            hh_id BIGINT UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            url VARCHAR(255)
        );
        """

        create_vacancies = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            hh_id BIGINT UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(8),
            url VARCHAR(255)
        );
        """

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(create_companies)
        cur.execute(create_vacancies)
        conn.commit()
        cur.close()
