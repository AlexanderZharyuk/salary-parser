from pprint import pprint
from typing import NamedTuple
from itertools import count

import requests

from tqdm import tqdm


class Vacancy(NamedTuple):
    total_pages: int
    total_vacancies: int


def get_vacancy(programmer_language: str, city_id: int) -> Vacancy:
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {programmer_language}',
        'area': city_id,
        'archived': False,
        'search_period': 30,
    }

    response = requests.get(url=url, params=params)
    response.raise_for_status()
    vacancies = response.json()

    return Vacancy(total_pages=vacancies['pages'],
                   total_vacancies=vacancies['found'])


def get_programmers_vacancies() -> dict:
    city_id = 1

    programmers_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'PHP',
                             'C++', 'C#']
    founded_vacancies = {}

    for language in tqdm(programmers_languages,
                         desc='Parse vacancies',
                         unit='vacancy'):
        vacancies = get_vacancy(
            programmer_language=language,
            city_id=city_id
        )
        vacancy_salaries = get_vacancy_salaries(language=language,
                                                pages=vacancies.total_pages)

        founded_vacancies[language] = {
            "vacancies_found": vacancies.total_vacancies,
            'vacancies_processed': vacancy_salaries.vacancies_processed,
            "average_salary": vacancy_salaries.average_salary
        }

    return founded_vacancies


class ProcessedVacancies(NamedTuple):
    average_salary: int
    vacancies_processed: int


def get_vacancy_salaries(language: str, pages: int) -> ProcessedVacancies:
    city_id = 1
    url = 'https://api.hh.ru/vacancies'

    processed_vacancies_salaries = []
    for page in count(0):
        if page >= pages:
            break

        params = {
            'text': f'Программист {language}',
            'area': city_id,
            'archived': False,
            'search_period': 30,
            'page': page,
        }

        response = requests.get(url=url, params=params)
        response.raise_for_status()
        vacancies = response.json()['items']
        for vacancy in vacancies:
            if predict_rub_salary(vacancy) is not None:
                processed_vacancies_salaries.append(vacancy)

    vacancies_processed = len(processed_vacancies_salaries)
    all_salaries = [predict_rub_salary(vacancy) for vacancy in
                    processed_vacancies_salaries if
                    predict_rub_salary(vacancy) is not None]
    average_salary = int(sum(all_salaries) / len(all_salaries))

    return ProcessedVacancies(average_salary=average_salary,
                              vacancies_processed=vacancies_processed)


def predict_rub_salary(vacancy: dict) -> float | None:
    vacancy_salary = vacancy['salary']

    if vacancy_salary is None or vacancy_salary['currency'] != 'RUR':
        return None
    elif vacancy_salary['from'] is None:
        return vacancy_salary['to'] * 0.8
    elif vacancy_salary['to'] is None:
        return vacancy_salary['from'] * 1.2

    return (vacancy_salary['from'] + vacancy_salary['to']) / 2


if __name__ == '__main__':
    pprint(get_programmers_vacancies())
