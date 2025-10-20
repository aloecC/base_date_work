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


class ParserConnection(Parser):
    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []
        self.__status = False

    def __connect(self):
        """Установка соединение с API (проверка доступности)."""
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            self.__status = True
        else:
            print(f"Ошибка при запросе: {response.status_code} - {response.text}")

    def connect(self) -> None:
        """Публичный метод подключения к API."""
        return self.__connect()


class ParserGetInfo(ParserConnection):
    def __init__(self):
        super().__init__()
        self.__vacancies_company =[]

    def fetch_company_details(self, hh_company_id):
        """Получение данных о компании."""
        pass

    def fetch_company_vacancies(self, hh_company_id, page):
        """Получение вакансий компании с постраничной загрузкой"""
        self.__vacancies_company = []
        self.__params['text'] = hh_company_id
        self.__params['page'] = page
        self.__connect()
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        self.__vacancies_company = response.json().get('items', [])
        return self.__vacancies_company
