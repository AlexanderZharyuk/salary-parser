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


if __name__ == '__main__':
    pprint(get_programmers_vacancies())