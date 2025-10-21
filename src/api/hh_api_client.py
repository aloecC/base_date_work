from abc import ABC, abstractmethod
import requests
from typing import List, Dict


class Parser(ABC):
    """
    Абстрактный базовый класс для работы с API сервисов вакансий.
    """

    @abstractmethod
    def connect(self) -> None:
        """Установка соединение с API (проверка доступности)."""
        pass

    @abstractmethod
    def search_employers(self, name: str, page: int = 0, per_page: int = 20) -> List[Dict]:
        """
        Поиск компаний (работодателей) по имени.
        Возвращает список компаний (items).
        """
        pass

    @abstractmethod
    def get_hh_company(self, data_company: List[Dict]) -> str or int:
        """Получение данных о компании."""
        pass

    @abstractmethod
    def fetch_company_vacancies(self, hh_company_id: str, page) -> list[dict]:
        """Получение вакансий компании с постраничной загрузкой"""
        pass


class ParserConnection(Parser):
    BASE_URL = "https://api.hh.ru/"

    def __init__(self):
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 20}
        self.__data_company = []
        self.__info_the_company = []
        self.__vacancies_company = []
        self.__status = False

    def __connect(self):
        """Установка соединение с API (проверка доступности)."""
        url = f"{self.BASE_URL}employers"
        response = requests.get(url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            self.__status = True
            return True
        else:
            print(f"Ошибка при запросе: {response.status_code} - {response.text}")

    def connect(self) -> bool:
        """Публичный метод подключения к API."""
        return self.__connect()

    def search_employers(self, name_company: str, page: int = 0, per_page: int = 20) -> List[Dict]:
        """
        Поиск компаний (работодателей) по имени.
        Возвращает список компаний (self.__data_company).
        """
        url = f"{self.BASE_URL}employers"
        params = {"text": name_company, "page": page, "per_page": per_page}
        resp = requests.get(url, headers=self.__headers, params=params, timeout=15)
        if resp.status_code != 200:
            raise RuntimeError(f"Ошибка запроса к HH: {resp.status_code} - {resp.text}")

        data = resp.json() or {}
        items = data.get('items', [])
        open_vacancies_available = False

        if isinstance(data.get('open_vacancies'), int):
            open_vacancies_available = data['open_vacancies'] > 0
        filtered = []
        for item in items:

            if isinstance(item, dict) and item.get('open_vacancies') is not None:
                if int(item.get('open_vacancies', 0)) > 0:
                    filtered.append(item)
            else:
                if item.get('id') is not None:
                    filtered.append(item)
        if not filtered:
            # fallback: если open_vacancies ключ присутствует и > 0
            if isinstance(data.get('open_vacancies'), int) and data['open_vacancies'] > 0:
                filtered = items

        self.__data_company = filtered
        return self.__data_company

    def get_hh_company(self, data_company: List[Dict]) -> str or int:
        """Получение  компании по максимальному количеству открытых вакансий"""
        company_max_open_vacancies = 0
        base_company = {}
        for company in data_company:
            if int(company['open_vacancies']) > company_max_open_vacancies:
                company_max_open_vacancies = int(company['open_vacancies'])
                base_company = company
        return base_company

    def get_str_hh_company(self, base_company: dict) -> str:
        """Получение строчного вывода информации о компании"""
        return (f'Название компании: {base_company["name"]}, '
                f' url: {base_company["url"]}, '
                f'Количество открытых вакансий: {base_company["open_vacancies"]}')

    def fetch_company_vacancies(self, company_id: str,  page: int = 0, per_page: int = 20) -> list[dict]:
        """Получение вакансий компании с постраничной загрузкой"""
        url = f"{self.BASE_URL}vacancies"
        params = {"employer_id": str(company_id), "page": page, "per_page": per_page}
        resp = requests.get(url, headers=self.__headers, params=params, timeout=15)
        if resp.status_code != 200:
            raise RuntimeError(f"Ошибка запроса к HH: {resp.status_code} - {resp.text}")
        self.__info_the_company = resp.json().get("items", [])
        return self.__info_the_company


