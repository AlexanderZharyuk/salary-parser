import time
from typing import NamedTuple
from itertools import count

import requests

from tqdm import tqdm

from general_functions import create_table, predict_salary


def get_programmers_vacancies(program_languages: list) -> dict:
    founded_vacancies = {}
    progress_bar = tqdm(program_languages,
                        miniters=1,
                        unit='program_language',
                        desc='HeadHunter vacancies')

    for language in progress_bar:
        tqdm.write(f'Parsing {language} vacancies...')
        vacancy_salaries = get_vacancy_salaries(language=language)

        founded_vacancies[language] = {
            "vacancies_found": vacancy_salaries.total_vacancies,
            'vacancies_processed': vacancy_salaries.vacancies_processed,
            "average_salary": vacancy_salaries.average_salary
        }

    return founded_vacancies


class ProcessedVacancies(NamedTuple):
    total_vacancies: int
    average_salary: int
    vacancies_processed: int


def get_vacancy_salaries(language: str) -> ProcessedVacancies:
    url = 'https://api.hh.ru/vacancies'
    moscow_city_id = 1
    during_time_in_days = 30

    params = {
        'text': f'Программист {language}',
        'area': moscow_city_id,
        'archived': False,
        'search_period': during_time_in_days,
    }

    pages = 1
    processed_vacancies_salaries = []
    for page in count(0):
        if page >= pages:
            break

        params['page'] = page
        try:
            response = requests.get(url=url, params=params)
            response.raise_for_status()
        except requests.ConnectionError:
            print('Get ConnectionError. Going to sleep 1 min')
            time.sleep(60)
            continue
        except requests.HTTPError:
            print('Get HttpError. Trying reconnect...')
            continue

        api_response = response.json()
        pages = api_response['pages']
        vacancies = api_response['items']
        for vacancy in vacancies:
            vacancy_salary = predict_rub_salary(vacancy)
            if vacancy_salary:
                processed_vacancies_salaries.append(vacancy_salary)

    total_vacancies = api_response['found']
    vacancies_processed = len(processed_vacancies_salaries)
    try:
        average_salary = int(sum(processed_vacancies_salaries) /
                             len(processed_vacancies_salaries))
    except ZeroDivisionError:
        average_salary = 0

    return ProcessedVacancies(average_salary=average_salary,
                              vacancies_processed=vacancies_processed,
                              total_vacancies=total_vacancies)


def predict_rub_salary(vacancy: dict) -> float | None:
    vacancy_salary = vacancy['salary']
    if not vacancy_salary or vacancy_salary['currency'] != 'RUR':
        return None

    vacancy_salary_from = vacancy_salary['from']
    vacancy_salary_to = vacancy_salary['to']

    return predict_salary(salary_from=vacancy_salary_from,
                          salary_to=vacancy_salary_to)


def parse_hh_vacancies() -> dict:
    programming_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'PHP',
                             'C++', 'C#']
    return get_programmers_vacancies(program_languages=programming_languages)


def main() -> None:
    hh_table_title = 'HeadHunter Moscow'
    print(create_table(vacancies=parse_hh_vacancies(),
                       table_title=hh_table_title))


if __name__ == '__main__':
    main()
