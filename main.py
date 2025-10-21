import os
from config import config
from src.api.hh_api_client import ParserConnection


def main():
    params = config()
    dsn = "dbname=hh_db user=postgres password=pass host=localhost port=5432"
    hh_api = ParserConnection()
    name_company = 'Sunlight'
    data_company = hh_api.search_employers(name_company)
    hh_api.connect()# Проверка соединения
    base_company = hh_api.get_hh_company(data_company)# Получение компании с наибольшем количеством открытых вакансий
    company_id = base_company['id']# Получение id компании
    data_info_company = hh_api.get_str_hh_company(base_company) #Строчное отображение информации о компании
    data_info_vacancies = hh_api.fetch_company_vacancies(company_id) #Получение вакансий компании по id компании



    #create_datebase('hh', params)
    #save_data_to_database(data_info_company, 'hh', params)

print(main())
