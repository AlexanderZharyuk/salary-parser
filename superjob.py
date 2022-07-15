import time

from itertools import count

import requests

from tqdm import tqdm

from general_functions import show_table, get_superjob_secret_key


def get_vacancies(secret_key: str, keywoard: str) -> dict:
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key,
    }
    moscow_city_id = 4
    results_per_request = 20

    total_salaries = []
    for page in count(0):
        params = {
            'town': moscow_city_id,
            'keyword': keywoard,
            'page': page,
            'count': results_per_request,
        }

        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
        except requests.ConnectionError:
            print('Get ConnectionError. Going to sleep 1 min.')
            time.sleep(60)
            continue
        except requests.HTTPError:
            print('Get HttpError. Trying reconnect...')
            continue

        response_json = response.json()
        vacancies_on_page = response_json['objects']

        if not vacancies_on_page:
            total_vacancies = response_json['total']
            vacancies_processed = len(total_salaries)
            average_salary = int(sum(total_salaries) / vacancies_processed)
            programing_language_vacancies = {
                'vacancies_found': total_vacancies,
                'vacancies_processed': vacancies_processed,
                'average_salary': average_salary
            }
            return programing_language_vacancies

        for vacancy in vacancies_on_page:
            vacancy_salary = predict_rub_salary(vacancy)
            if vacancy_salary:
                total_salaries.append(vacancy_salary)


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


def parse_superjob_vacancies(secret_key: str) -> dict:
    programming_languages = ['Javascript', 'Java', 'Python', 'Ruby',
                             'PHP', 'C++', 'C#']

    vacancies = {}
    progress_bar = tqdm(programming_languages,
                        miniters=1,
                        unit='program_language',
                        desc='SuperJob vacancies')

    for language in progress_bar:
        tqdm.write(f'Parsing {language} vacancies...')
        vacancies[language] = get_vacancies(keywoard=language,
                                            secret_key=secret_key)

    return vacancies


def main() -> None:
    superjob_secret_key = get_superjob_secret_key()
    superjob_table_title = 'SuperJob Moscow'
    show_table(vacancies=parse_superjob_vacancies(superjob_secret_key),
               table_title=superjob_table_title)


if __name__ == '__main__':
    main()
