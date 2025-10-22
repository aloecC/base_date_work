from config import config
from src.api.hh_api_client import ParserConnection
from src.handler_file.sql_handler import DBManager, DBManagerWorker


def main():
    params = config()
    hh_api = ParserConnection()
    db_user = DBManager()
    name_bd = 'hh'  # для проверки
    names_companies = [
        'Topface Media', 'Polza Agency',
        'ООО ПК Техномикс', 'Aston',
        'ООО Софтвайс', 'Латера',
        'FINAMP', 'Keep Calm',
        'Extyl', 'ООО Электронная медицина'
    ]  # для проверки

    keywords = ['Python', 'SQL', 'Django']  # для проверки
    company_id = 18239  # для проверки

    data_company = hh_api.search_employers(names_companies)  #Получение всех компаний с подходящим названием
    hh_api.connect()  # Проверка соединения
    #base_company = hh_api.get_hh_company(company_id, data_company)# Получение компании по id

    #hh_api.fetch_company_vacancies(str(company_id))  # Получение вакансий компании по id компании
    #data_str_company = hh_api.get_str_hh_company(base_company) #Строчное отображение информации о компании)

    db_user.create_datebase(name_bd, params)  #Создание бд и таблиц
    db_user.save_data_to_bd(data_company, name_bd, params)  #Добавление и сохранение данных

    bd_worker = DBManagerWorker()

    companies_and_vacancies_count = bd_worker.get_companies_and_vacancies_count(name_bd, params)
    all_vacancies = bd_worker.get_all_vacancies(name_bd, params)
    avg_salary = bd_worker.get_avg_salary(name_bd, params)
    vacancies_with_higher_salary = bd_worker.get_vacancies_with_higher_salary(name_bd, params)
    vacancies_with_keyword = bd_worker.get_vacancies_with_keyword(name_bd, params, keywords)

    #строчное отображение
    companies_and_vacancies_count_str = bd_worker.get_companies_and_vacancies_count_str(companies_and_vacancies_count)
    all_vacancies_str = bd_worker.get_all_vacancies_str(all_vacancies)
    avg_salary_str = bd_worker.get_avg_salary_str(avg_salary)
    vacancies_with_higher_salary_str = bd_worker.get_vacancies_with_higher_salary_str(vacancies_with_higher_salary)
    vacancies_with_keyword_str = bd_worker.get_vacancies_with_keyword_str(vacancies_with_keyword)


print(main())
