from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:
    hh_id: int
    name: str
    url: Optional[str] = None
    open_vacancies: int = 0


@dataclass
class Vacancy:
    hh_id: int
    name: str
    company_id: int
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    currency: Optional[str] = None
    url: Optional[str] = None