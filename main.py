import os
from config import config
from src.api.hh_api_client import ParserConnection
from src.models.vacancy_servise import Vacancy


def main():
    params = config()
    hh_api = ParserConnection()
    name_company = 'Sunlight'
    data_company = hh_api.search_employers(name_company)
    hh_api.connect()# Проверка соединения
    base_company = hh_api.get_hh_company(data_company)# Получение компании с наибольшем количеством открытых вакансий
    company_id = base_company['id']# Получение id компании
    data_info_company = hh_api.get_str_hh_company(base_company) #Строчное отображение информации о компании
    data_info_vacancies = hh_api.fetch_company_vacancies(company_id)

    filtered_vacancies = Vacancy.get_filtered_vacancies(data_info_vacancies)#Получение списка обьектов вакансий
    data_str_info_vacancies = Vacancy.cast_to_object_list(filtered_vacancies)#Строчное отображение информации о вакансиях

    for info in data_str_info_vacancies:
        print(info)#Построчный вывод информации о вакансиях компании

    #create_datebase('hh', params)
    #save_data_to_database(data_info_company, 'hh', params)

print(main())
