import psycopg2
from psycopg2 import sql
from typing import List, Tuple, Optional
from src.models.company_and_vacancy_servise import Company, Vacancy
from config import config


class DBManager:
    """
    Класс для работы с PostgreSQL.
    """
    def create_datebase(self, name_db: str, params: dict) -> None:
        """Создание базы данных HH.ru"""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {name_db}')
        cur.execute(f'CREATE DATABASE {name_db}')

        cur.close()
        conn.close()

        with psycopg2.connect(dbname=name_db, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS companies (
                        id SERIAL PRIMARY KEY,
                        hh_id BIGINT UNIQUE NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        url VARCHAR(255)
                    )
                """)

            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        hh_id BIGINT UNIQUE NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        currency VARCHAR(8),
                        url VARCHAR(255)
                    )
                """)

        conn.commit()

    def save_data_company(self, data_company, name_bd, params):
        pass

    def save_data_vacancy(self, data_info_vacancies, name_bd, params):
        pass

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass

