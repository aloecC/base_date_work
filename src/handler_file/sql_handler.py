import psycopg2
from typing import List, Dict

from src.api.hh_api_client import ParserConnection


class DBManager(ParserConnection):
    """
    Класс для работы с PostgreSQL(Создание и сохранение).
    """

    def create_datebase(self, name_bd: str, params: dict) -> None:
        """Создание базы данных HH.ru"""

        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {name_bd}")
        cur.execute(f"CREATE DATABASE {name_bd}")

        cur.close()
        conn.close()

        with psycopg2.connect(dbname=name_bd, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS companies (
                        id SERIAL PRIMARY KEY,
                        hh_id BIGINT UNIQUE NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        url VARCHAR(255)
                    )
                """
                )

            with conn.cursor() as cur:
                cur.execute(
                    """
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
                """
                )

        conn.commit()

    def save_data_to_bd(
        self, data_company: List[Dict], name_bd: str, params: dict
    ) -> None:
        """Сохранение данных в таблицы"""
        conn = psycopg2.connect(dbname=name_bd, **params)
        with conn.cursor() as cur:
            for company in data_company:
                company_hh_id = company["id"]
                company_name = company["name"]
                company_url = company["url"]
                cur.execute(
                    """
                    INSERT INTO companies(hh_id, name, url)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (company_hh_id, company_name, company_url),
                )
                company_db_id = cur.fetchone()[0]
                data_info_vacancies = ParserConnection.fetch_company_vacancies(
                    self, str(company_hh_id)
                )

                for vacancy in data_info_vacancies:
                    vacancy_hh_id = vacancy.get("id")
                    vacancy_name = vacancy.get("name")

                    salary_info = vacancy.get("salary") or {}
                    vacancy_salary_from = salary_info.get("from")
                    vacancy_salary_to = salary_info.get("to")
                    vacancy_currency = salary_info.get("currency")
                    vacancy_url = vacancy.get("url")
                    cur.execute(
                        """
                        INSERT INTO vacancies(hh_id, name, company_id, salary_from, salary_to, currency, url)
                        VALUES (%s, %s, %s,%s, %s, %s, %s)
                        """,
                        (
                            vacancy_hh_id,
                            vacancy_name,
                            company_db_id,
                            vacancy_salary_from,
                            vacancy_salary_to,
                            vacancy_currency,
                            vacancy_url,
                        ),
                    )

        conn.commit()
        conn.close()


class DBManagerWorker:
    """
    Класс для работы с PostgreSQL.
    """

    def get_companies_and_vacancies_count(self, name_bd: str, params: dict):
        """Получение списка всех компаний
        и количества вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=name_bd, **params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.name,
                    COUNT(v.hh_id) AS vacancy_count
                FROM
                    companies AS c
                LEFT JOIN
                    vacancies AS v
                    ON v.company_id = c.id
                GROUP BY
                    c.id;
                """
            )
            columns = [desc[0] for desc in cur.description]
            results = [dict(zip(columns, row)) for row in cur.fetchall()]

        conn.commit()
        return results
        conn.close()

    def get_companies_and_vacancies_count_str(
        self, companies_and_vacancies_count: List[Dict]
    ) -> None:
        """Получение строки всех компаний
        и количества вакансий у каждой компании."""
        for result in companies_and_vacancies_count:
            print(
                f'Компания:{result["name"]}, Количество вакансий: {result["vacancy_count"]}'
            )

    def get_all_vacancies(self, name_bd: str, params: dict):
        """Получение списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=name_bd, **params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.name as company_name,
                    v.name as vacancy_name,
                    v.salary_from, v.salary_to,
                    v.url as vacancy_url
                FROM
                    companies AS c
                LEFT JOIN
                    vacancies AS v
                    ON v.company_id = c.id
                """
            )
            columns = [desc[0] for desc in cur.description]
            results = [dict(zip(columns, row)) for row in cur.fetchall()]

        conn.commit()
        return results
        conn.close()

    def get_all_vacancies_str(self, all_vacancies: List[Dict]) -> None:
        """Получение строки всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        for vacancy in all_vacancies:
            print(
                f'Компания: {vacancy["company_name"]}, Вакансия: {vacancy["vacancy_name"]},'
                f' Зарплата: от {vacancy["salary_from"]}'
                f' до {vacancy["salary_to"]}, Ссылка: {vacancy["vacancy_url"]}'
            )

    def get_avg_salary(self, name_bd: str, params: dict):
        """Получение средний зарплаты по вакансиям."""
        conn = psycopg2.connect(dbname=name_bd, **params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ROUND(AVG(v.salary_from),2) as avg_salary_from,
                    ROUND(AVG(v.salary_to),2) as avg_salary_to
                FROM
                    companies AS c
                LEFT JOIN
                    vacancies AS v
                    ON v.company_id = c.id
                """
            )
            columns = [desc[0] for desc in cur.description]
            results = [dict(zip(columns, row)) for row in cur.fetchall()]

        conn.commit()
        return results
        conn.close()

    def get_avg_salary_str(self, avg_salary: List[Dict]) -> None:
        """Получение строчного отображения средний зарплаты по вакансиям."""
        for result in avg_salary:
            print(
                f'Средняя зарплата от {result["avg_salary_from"]} до {result["avg_salary_to"]}'
            )

    def get_vacancies_with_higher_salary(self, name_bd: str, params: dict):
        """Получение списка всех вакансий,
        у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=name_bd, **params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    v.name
                FROM
                    vacancies v
                WHERE
                    v.salary_from > (SELECT AVG(salary_from) FROM vacancies)
                    OR v.salary_to > (SELECT AVG(salary_to) FROM vacancies);
                """
            )
            columns = [desc[0] for desc in cur.description]
            results = [dict(zip(columns, row)) for row in cur.fetchall()]

        conn.commit()
        return results
        conn.close()

    def get_vacancies_with_higher_salary_str(
        self, vacancies_with_higher_salary: List[Dict]
    ) -> None:
        """Получение строки всех вакансий,
        у которых зарплата выше средней по всем вакансиям."""
        for vacancy in vacancies_with_higher_salary:
            print(f'Вакансия: {vacancy["name"]}')

    def get_vacancies_with_keyword(self, name_bd: str, params: dict, keywords: list):
        """Получение списка всех вакансий,
        в названии которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(dbname=name_bd, **params)
        try:
            with conn.cursor() as cur:
                # Строим условие: v.name ILIKE '%word1%'
                # OR v.name ILIKE '%word2%' .
                conditions = []
                for word in keywords:
                    # Экранируем одинарные кавычки в слове,
                    # чтобы корректно вставить в SQL
                    w = word.replace("'", "''")
                    conditions.append(f"v.name ILIKE '%{w}%'")
                where_clause = " OR ".join(conditions) if conditions else "FALSE"

                cur.execute(
                    f"""
                        SELECT
                            v.name AS vacancy_name,
                            v.id AS vacancy_id,
                            c.id AS company_id,
                            c.name AS company_name,
                            v.url
                        FROM
                            companies AS c
                        LEFT JOIN
                            vacancies AS v ON v.company_id = c.id
                        WHERE
                            {where_clause}
                        """
                )
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in cur.fetchall()]
            conn.commit()
            return results
        finally:
            conn.close()

    def get_vacancies_with_keyword_str(
        self, vacancies_with_keyword: List[Dict]
    ) -> None:
        """Получение строки всех вакансий,
        в названии которых содержатся переданные в метод слова"""
        for vacancy in vacancies_with_keyword:
            print(
                f'Вакансия: {vacancy["vacancy_name"]},Компания: {vacancy["company_name"]}, Ссылка:{vacancy["url"]}'
            )
