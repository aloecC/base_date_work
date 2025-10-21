from typing import List
from src.api.hh_api_client import ParserConnection


class Vacancy(ParserConnection():

    __slots__ = ("_name", "_url", "_salary", "_requirements")

    def __init__(self, name: str, url: str, salary=None, requirement: str = ""):
        super().__init__()
        self._name = self._validate_name(name)
        self._url = self._validate_url(url)
        self._salary = self._validate_salary(salary)
        self._requirement = self._validate_requirement(requirement)
        self.__lst_vacancy = []  # список объектов вакансий

    def _validate_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название вакансии должно быть непустой строкой.")
        return value.strip()

    def _validate_url(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("URL вакансии должно быть непустой строкой.")
        return value.strip()

    def _validate_salary(self, value):
        # Принятое поведение:
        # {'from': 1000, 'to': 2000, 'currency': 'USD', 'gross': True} или
        if isinstance(value, str):
            return value.strip()

        if value is None:
            return 0

        if value['to'] is not None:
            if isinstance(value['from'], (int, float)) and isinstance(value['to'], (int, float)):
                if value['from'] < 0 or value['to'] < 0:
                    raise ValueError("Зарплата не может быть отрицательной.")
                return f"{value['from']}-{value['to']}"
        if value['from'] is None:
            if isinstance(value['to'], (int, float)):
                return f"{value['to']}"
        return f"{value['from']}"

    def _validate_requirement(self, value):
        if value is None:
            return ""
        if not isinstance(value, str):
            raise ValueError("Requirement должны быть строкой.")
        return value.strip()

    # Свойства для доступа к приватным полям
    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary(self) -> float:
        return self._salary

    @property
    def requirement(self) -> str:
        return self._requirement