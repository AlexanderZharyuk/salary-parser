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


def get_programmers_vacancies(program_languages: list, city_id: int) -> dict:
    founded_vacancies = {}

    for language in tqdm(program_languages,
                         miniters=1,
                         unit='program_language',
                         desc='Parse hh vacancies'):
        tqdm.write(f'Parse {language} vacancies...')
        vacancies = get_vacancy(
            programmer_language=language,
            city_id=city_id
        )
        vacancy_salaries = get_vacancy_salaries(language=language,
                                                pages=vacancies.total_pages,
                                                city_id=city_id)

        founded_vacancies[language] = {
            "vacancies_found": vacancies.total_vacancies,
            'vacancies_processed': vacancy_salaries.vacancies_processed,
            "average_salary": vacancy_salaries.average_salary
        }

    return founded_vacancies


class ProcessedVacancies(NamedTuple):
    average_salary: int
    vacancies_processed: int


def get_vacancy_salaries(language: str, pages: int, city_id: int) \
        -> ProcessedVacancies:
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


def predict_salary(salary_from: int, salary_to: int) -> int | None:
    if not salary_from and not salary_to:
        return None
    elif not salary_from:
        return int(salary_to * 0.8)
    elif not salary_to:
        return int(salary_from * 1.2)

    return (salary_to + salary_from) // 2


def predict_rub_salary(vacancy: dict) -> float | None:
    vacancy_salary = vacancy['salary']
    if vacancy_salary is None or vacancy_salary['currency'] != 'RUR':
        return None

    vacancy_salary_from = vacancy_salary['from']
    vacancy_salary_to = vacancy_salary['to']

    return predict_salary(salary_from=vacancy_salary_from,
                          salary_to=vacancy_salary_to)


def parse_hh_vacancies():
    city_id = 1
    program_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'PHP',
                         'C++', 'C#']
    print(get_programmers_vacancies(program_languages=program_languages,
                                    city_id=city_id))


if __name__ == '__main__':
    parse_hh_vacancies()
