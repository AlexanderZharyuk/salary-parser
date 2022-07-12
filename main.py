from pprint import pprint

import requests


def get_programmers_vacancies() -> dict:
    programmers_id = 96
    city_id = 1

    url = 'https://api.hh.ru/vacancies'
    programmers_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'PHP',
                             'C++', 'C#', 'C', 'GO', 'Scala', 'Swift',
                             'Typescript']
    languages_vacancies = {}

    for language in programmers_languages:
        params = {
            'text': f'Программист {language}',
            'area': city_id,
            'professional_role': programmers_id,
            'per_page': 20,
            'archived': False,
            'search_period': 30
        }

        response = requests.get(url=url, params=params)
        response.raise_for_status()
        vacancies = response.json()
        languages_vacancies[language] = vacancies['found']

    return languages_vacancies


def get_python_vacancies_salaries() -> None:
    programmers_id = 96
    city_id = 1

    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'Программист Python',
        'area': city_id,
        'professional_role': programmers_id,
        'per_page': 20,
        'archived': False,
        'search_period': 30
    }

    response = requests.get(url=url, params=params)
    response.raise_for_status()
    vacancies = response.json()['items']

    for vacancy in vacancies:
        print(predict_rub_salary(vacancy))


def predict_rub_salary(vacancy: dict) -> int | None:
    vacancy_salary = vacancy['salary']

    if vacancy_salary is None or vacancy_salary['currency'] != 'RUR':
        return None
    elif vacancy_salary['from'] is None:
        return vacancy_salary['to'] * 0.8
    elif vacancy_salary['to'] is None:
        return vacancy_salary['from'] * 1.2

    return (vacancy_salary['from'] + vacancy_salary['to']) / 2


if __name__ == '__main__':
    print(get_python_vacancies_salaries())
