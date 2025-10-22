import unittest
from unittest.mock import patch, MagicMock

from src.handler_file.sql_handler import DBManagerWorker


class TestDBManagerWorker(unittest.TestCase):
    @patch("psycopg2.connect")
    def test_get_companies_and_vacancies_count(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        # Симулируем описание результатов
        mock_cursor.description = [("name",), ("vacancy_count",)]
        mock_cursor.fetchall.return_value = [
            ("Company A", 3),
            ("Company B", 1),
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        worker = DBManagerWorker()
        name_bd = "testdb"
        params = {}

        # Act
        result = worker.get_companies_and_vacancies_count(name_bd, params)

        # Assert
        expected = [
            {"name": "Company A", "vacancy_count": 3},
            {"name": "Company B", "vacancy_count": 1},
        ]
        self.assertEqual(result, expected)
        mock_connect.assert_called_once_with(dbname=name_bd, **params)

    @patch("psycopg2.connect")
    def test_get_all_vacancies(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("company_name",),
            ("vacancy_name",),
            ("salary_from",),
            ("salary_to",),
            ("vacancy_url",),
        ]
        mock_cursor.fetchall.return_value = [
            ("Company A", "Dev", 1000, 2000, "http://x"),
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        worker = DBManagerWorker()
        vacancies = worker.get_all_vacancies("testdb", {})

        self.assertEqual(
            vacancies,
            [{"company_name": "Company A", "vacancy_name": "Dev", "salary_from": 1000, "salary_to": 2000, "vacancy_url": "http://x"}]
        )

    @patch("psycopg2.connect")
    def test_get_avg_salary(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.description = [("avg_salary_from",), ("avg_salary_to",)]
        mock_cursor.fetchall.return_value = [(1500.0, 3000.0)]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        worker = DBManagerWorker()
        result = worker.get_avg_salary("testdb", {})

        self.assertEqual(result, [{"avg_salary_from": 1500.0, "avg_salary_to": 3000.0}])

    @patch("psycopg2.connect")
    def test_get_vacancies_with_higher_salary(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.description = [("name",)]
        mock_cursor.fetchall.return_value = [("Senior Dev",)]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        worker = DBManagerWorker()
        result = worker.get_vacancies_with_higher_salary("testdb", {})

        self.assertEqual(result, [{"name": "Senior Dev"}])

    @patch("psycopg2.connect")
    def test_get_vacancies_with_keyword(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("vacancy_name",),
            ("vacancy_id",),
            ("company_id",),
            ("company_name",),
            ("url",),
        ]
        mock_cursor.fetchall.return_value = [
            ("DevOps Engineer", 1, 1, "Company A", "http://x")
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        worker = DBManagerWorker()
        keywords = ["Dev", "Engineer"]
        result = worker.get_vacancies_with_keyword("testdb", {}, keywords)

        self.assertEqual(
            result,
            [{"vacancy_name": "DevOps Engineer", "vacancy_id": 1, "company_id": 1, "company_name": "Company A", "url": "http://x"}]
        )


if __name__ == "__main__":
    unittest.main()
