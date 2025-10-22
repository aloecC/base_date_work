# Парсинг вакансий hh.ru и хранение в PostgreSQL
Описание задачи:
Получить данные о работодателях и их вакансиях с сайта hh.ru через публичный API, спроектировать таблицы в БД PostgreSQL и загрузить данные в созданные таблицы. Реализовать набор классов и функций для взаимодействия с API, файлами и базой данных, обеспечить удобный интерфейс для пользователя и соответствие критериям оценки.
Список задач проекта

Получение данных о работодателях и вакансиях через API hh.ru с использованием requests.
Выбор  10 компаний для сбора вакансий.
Проектирование БД PostgreSQL: таблица компаний и таблица вакансий, связь через внешний ключ.
Реализация кода загрузки данных в таблицы БД.
Реализация класса DBManager для взаимодействия с PostgreSQL через psycopg2.
Реализация функций/модулей для взаимодействия с API, файлами и вакансиями.
Взаимодействие с пользователем через понятный интерфейс.

Соответствие требованиям SOLID (минимум первые два принципа), документация и типизация.

Архитектура проекта

hh_api_client.py — модуль для взаимодействия с публичным API hh.ru (получение данных о работодателях и вакансиях).
company_and_vacancy_service.py — объявление структур БД (органы и вакансии) и схемы.
sql_handler.py — реализация класса DBManager, подключение к PostgreSQL через psycopg2 и набор методов:
get_companies_and_vacancies_count()
get_all_vacancies()
get_avg_salary()
get_vacancies_with_higher_salary()
get_vacancies_with_keyword(keywords)

Также добавлены методы построчного отображения данных по таблицам:
get_companies_and_vacancies_count_str()
get_all_vacancies_str()
get_avg_salary_str()
get_vacancies_with_higher_salary_str()
get_vacancies_with_keyword_str(keywords)

sql_handler.py — модуль загрузки данных в БД: создание базы данных, создание таблиц, заполнение таблиц.
cli.py — точка входа и интерфейс взаимодействия с пользователем: запуск всего процесса, выбор компаний, просмотр результатов.
config.py — конфигурационные параметры: параметры подключения к БД, параметры API.
requirements.txt — зависимости проекта: requests, psycopg2-binary, pydantic (при необходимости), etc.
.gitignore — исключение временных файлов и артефактов.
README.md — это файл проекта с подробным описанием.

Детали реализации

API клиент (hh_api_client.py)

Используется библиотека requests.
Реализованы функции:
get_hh_company(company_id, data_company) — получение данных о компании.
fetch_company_vacancies(company_id, page) — получение вакансий компании с постраничной загрузкой.

Все данные нормализуются (поля приводятся к ожидаемым типам).

Модели БД и создание таблиц (sql_handler.py)

Таблица companies (id SERIAL PRIMARY KEY, hh_id BIGINT UNIQUE NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        url VARCHAR(255))

Таблица vacancies (id SERIAL PRIMARY KEY, hh_id BIGINT UNIQUE NOT NULL, name VARCHAR(255) NOT NULL,
                        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
                        salary_from INTEGER, salary_to INTEGER,
                        currency VARCHAR(8), url VARCHAR(255))

Внешний ключ между vacancies и companies реализован через company_id.

Код автоматического создания БД и таблиц вызывается из основного скрипта.

