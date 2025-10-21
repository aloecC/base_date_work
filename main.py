import os
from config import config
from src.api.hh_api_client import ParserConnection
from src.handler_file.sql_handler import DBManager


def main():
    params = config()
    hh_api = ParserConnection()
    db_user = DBManager()
    name_bd = 'hh'
    name_company = 'Sunlight'
    company_id = 18239
    data_company = hh_api.search_employers(name_company)#Получение всех компаний с подходящим названием
    hh_api.connect()# Проверка соединения
    base_company = hh_api.get_hh_company(company_id, data_company)# Получение компании по id

    print(base_company)
    data_info_vacancies = hh_api.fetch_company_vacancies(str(company_id))  # Получение вакансий компании по id компании

    data_str_company = hh_api.get_str_hh_company(base_company) #Строчное отображение информации о компании
    print(data_info_vacancies)

    #db_user.create_datebase(name_bd, params)
    #db_user.save_data_company(data_company, name_bd, params)

print(main())
