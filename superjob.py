import os

from itertools import count
from pprint import pprint

import requests

from tqdm import tqdm
from dotenv import load_dotenv


def get_vacancies(secret_key: str, keywoard: str) -> dict:
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key,
    }

    total_salaries = []
    for page in count(0):
        params = {
            'town': 4,
            'keyword': keywoard,
            'page': page,
            'count': 20,
        }

        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()

        vacancies_on_page = response.json()['objects']

        if not len(vacancies_on_page):
            total_vacancies = response.json()['total']
            vacancies_processed = len(total_salaries)
            average_salary = int(sum(total_salaries) / vacancies_processed)
            program_language_vacancies = {
                'vacancies_found': total_vacancies,
                'vacancies_processed': vacancies_processed,
                'average_salary': average_salary
            }
            return program_language_vacancies

        for vacancy in vacancies_on_page:
            if predict_rub_salary(vacancy) is not None:
                total_salaries.append(predict_rub_salary(vacancy))


def predict_salary(salary_from: int, salary_to: int) -> int | None:
    if not salary_from and not salary_to:
        return None
    elif not salary_from:
        return int(salary_to * 0.8)
    elif not salary_to:
        return int(salary_from * 1.2)

    return (salary_to + salary_from) // 2


def predict_rub_salary(vacancy: dict) -> int | None:
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    if vacancy['currency'] != 'rub':
        return None

    return predict_salary(salary_from=salary_from, salary_to=salary_to)


def main():
    load_dotenv()
    superjob_secret_key = os.environ['SUPERJOB_SECRET_KEY']
    programmers_languages = ['Javascript', 'Java', 'Python', 'Ruby',
                             'PHP', 'C++', 'C#']

    vacancies = {}
    progress_bar = tqdm(programmers_languages,
                        miniters=1,
                        unit='program_language',
                        desc='SuperJob vacancies')

    for language in progress_bar:
        tqdm.write(f'Parse {language} vacancies...')
        vacancies[language] = get_vacancies(keywoard=language,
                                            secret_key=superjob_secret_key)

    pprint(vacancies)


if __name__ == '__main__':
    main()