import psycopg2
from psycopg2 import sql
from typing import List, Tuple, Optional, Dict

from src.api.hh_api_client import ParserConnection
from src.models.company_and_vacancy_servise import Company, Vacancy
from config import config


class DBManager(ParserConnection):
    """
    Класс для работы с PostgreSQL.
    """
    def create_datebase(self, name_bd: str, params: dict) -> None:
        """Создание базы данных HH.ru"""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {name_bd}')
        cur.execute(f'CREATE DATABASE {name_bd}')

        cur.close()
        conn.close()

        with psycopg2.connect(dbname=name_bd, **params) as conn:
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

    def save_data_to_bd(self, data_company: List[Dict], name_bd: str, params: dict) -> None:
        """Сохранение данных в таблицы"""
        conn = psycopg2.connect(dbname=name_bd, **params)
        with conn.cursor() as cur:
            for company in data_company:
                company_hh_id = company['id']
                company_name = company['name']
                company_url = company['url']
                cur.execute(
                    """
                    INSERT INTO companies(hh_id, name, url)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (company_hh_id, company_name, company_url)
                )
                company_db_id = cur.fetchone()[0]
                data_info_vacancies = ParserConnection.fetch_company_vacancies(self, str(company_hh_id))

                for vacancy in data_info_vacancies:
                    vacancy_hh_id = vacancy.get('id')
                    vacancy_name = vacancy.get('name')

                    salary_info = vacancy.get('salary') or {}
                    vacancy_salary_from = salary_info.get('from')
                    vacancy_salary_to = salary_info.get('to')
                    vacancy_currency = salary_info.get('currency')
                    vacancy_url = vacancy.get('url')
                    cur.execute(
                        """
                        INSERT INTO vacancies(hh_id, name, company_id, salary_from, salary_to, currency, url)
                        VALUES (%s, %s, %s,%s, %s, %s, %s)
                        """,
                        (vacancy_hh_id, vacancy_name, company_db_id, vacancy_salary_from, vacancy_salary_to, vacancy_currency, vacancy_url)
                    )

        conn.commit()
        conn.close()



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

