import os
from config import config
from src.api.hh_api_client import ParserConnection


def main():
    params = config()
    hh_api = ParserConnection()
    name_company = 'Sunlight'
    data_company = hh_api.search_employers(name_company)
    hh_api.connect()
    base_company = hh_api.get_hh_company(data_company)
    company_id = base_company['id']
    data_info_company = hh_api.get_str_hh_company(base_company)
    data_info_vacancies = hh_api.fetch_company_vacancies(company_id)
    return data_info_vacancies
    #create_datebase('hh', params)
    #save_data_to_database(data_info_company, 'hh', params)

print(main())
