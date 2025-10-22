import unittest
from unittest.mock import patch, MagicMock
from typing import List, Dict

from abc import ABC, abstractmethod

from src.api.hh_api_client import ParserConnection


# Исходный код (которые вы предоставили) импортируется как модуль, например mymodule
# from mymodule import Parser, ParserConnection

# Для локального теста можно определить минимальные заглушки:
class Parser(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def search_employers(self, name: str, page: int = 0, per_page: int = 20) -> List[Dict]:
        pass

    @abstractmethod
    def get_hh_company(self, company_id, data_company: List[Dict]) -> str or int:
        pass

    @abstractmethod
    def fetch_company_vacancies(self, hh_company_id: str, page) -> list[dict]:
        pass


class TestParserConnection(unittest.TestCase):

    @patch("requests.get")
    def test_connect_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp

        pc = ParserConnection()
        self.assertTrue(pc.connect())

        mock_get.assert_called_once()

    @patch("requests.get")
    def test_connect_failure(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.text = "Not Found"
        mock_get.return_value = mock_resp

        pc = ParserConnection()
        self.assertFalse(pc.connect())

    @patch("requests.get")
    def test_search_employers_filters_and_collect(self, mock_get):
        # Сценарий: один запрос, items содержит несколько форматов
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "items": [
                {"id": 1, "name": "A", "open_vacancies": "5", "url": "u1"},
                {"id": 2, "name": "B", "open_vacancies": 0, "url": "u2"},
                {"id": 3, "name": "C", "url": "u3"},
            ],
        }
        mock_get.return_value = mock_resp

        pc = ParserConnection()
        result = pc.search_employers(["A"], page=0, per_page=20)

        # Ожидаем, что вернется список компаний, и в него попала первая подходящая запись
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)
        self.assertIn({"id": 1, "name": "A", "open_vacancies": "5", "url": "u1"}, result)

    @patch("requests.get")
    def test_search_employers_error_status(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "Server Error"
        mock_get.return_value = mock_resp

        pc = ParserConnection()
        with self.assertRaises(RuntimeError):
            pc.search_employers(["X"])

    @patch("requests.get")
    def test_get_hh_company(self, mock_get):
        data = [
            {"id": 10, "name": "Comp", "url": "u", "open_vacancies": 2},
            {"id": 20, "name": "Other", "url": "u2", "open_vacancies": 0},
        ]
        pc = ParserConnection()
        res = pc.get_hh_company(20, data)
        self.assertEqual(res, data[1])

    def test_get_str_hh_company(self):
        base = {"name": "Comp", "url": "http://x", "open_vacancies": 3}
        pc = ParserConnection()
        self.assertIn("Название компании: Comp", pc.get_str_hh_company(base))

    @patch("requests.get")
    def test_fetch_company_vacancies_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"items": [{"id": "v1"}, {"id": "v2"}]}
        mock_get.return_value = mock_resp

        pc = ParserConnection()
        res = pc.fetch_company_vacancies("123", page=0)
        self.assertIsInstance(res, list)
        self.assertEqual(res, [{"id": "v1"}, {"id": "v2"}])

    @patch("requests.get")
    def test_fetch_company_vacancies_failure(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        mock_resp.text = "Forbidden"
        mock_get.return_value = mock_resp

        pc = ParserConnection()
        with self.assertRaises(RuntimeError):
            pc.fetch_company_vacancies("123", page=0)


class TestAbstractParser(unittest.TestCase):
    def test_abstract_methods_enforced(self):
        # попытаемся инстанцировать абстрактный класс напрямую
        with self.assertRaises(TypeError):
            Parser()


if __name__ == "__main__":
    unittest.main()
