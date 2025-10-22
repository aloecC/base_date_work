from config import config
from src.api.hh_api_client import ParserConnection
from src.handler_file.sql_handler import DBManager, DBManagerWorker


def user_worker():
    '''Функция для взаимодействия с пользователем'''
    params = config()
    hh_api = ParserConnection()
    db_user = DBManager()
    bd_worker = DBManagerWorker()
    platforms = ["HeadHunter"]
    print(f'Здравствуйте! Мы на платформе {platforms}, Давайте подберем вам работу!')

    name_bd = input("Введите имя базы данных:")

    names_companies = []
    for num in range(10):
        word = input(f"Введите название компании(осталось {10 - num} из 10): ")
        names_companies.append(word)

    keywords = input('Введите слова для поиска через пробел: ').split(' ')

    data_company = hh_api.search_employers(names_companies)  #Получение всех компаний с подходящим названием

    db_user.create_datebase(name_bd, params)  #Создание бд и таблиц
    db_user.save_data_to_bd(data_company, name_bd, params)  #Добавление и сохранение данных
    print("Компнии и количество их открытых вакансий:")
    companies_and_vacancies_count_str = (
        bd_worker.get_companies_and_vacancies_count_str(bd_worker.get_companies_and_vacancies_count(name_bd, params)))
    print("Все вакансии компаний:")
    all_vacancies_str = (
        bd_worker.get_all_vacancies_str(bd_worker.get_all_vacancies(name_bd, params)))
    print("Средняя зарплата по вакансиям:")
    avg_salary_str = (
        bd_worker.get_avg_salary_str(bd_worker.get_avg_salary(name_bd, params)))
    print("Вакансии с зарплатой выше среднего:")
    vacancies_with_higher_salary_str = (
        bd_worker.get_vacancies_with_higher_salary_str(bd_worker.get_vacancies_with_higher_salary(name_bd, params)))
    print("Ваши вакансии по результату запроса:")
    vacancies_with_keyword_str = (
        bd_worker.get_vacancies_with_keyword_str(bd_worker.get_vacancies_with_keyword(name_bd, params, keywords)))


name_bd = 'hh'  # для проверки
names_companies = [
    'Topface Media', 'Polza Agency',
    'ООО ПК Техномикс', 'Aston',
    'ООО Софтвайс', 'Латера',
    'FINAMP', 'Keep Calm',
    'Extyl', 'ООО Электронная медицина'
]  # для проверки

keywords = "Python SQL Django"  # для проверки

user_worker()
