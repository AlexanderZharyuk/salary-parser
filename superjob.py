import os

import requests

from dotenv import load_dotenv


def get_vacancies(secret_key: str) -> list:
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key,
    }

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    vacanices = response.json()['objects']
    professions = [vacancy['profession'] for vacancy in vacanices]

    return professions


if __name__ == '__main__':
    load_dotenv()
    superjob_secret_key = os.environ['SUPERJOB_SECRET_KEY']
    vacancies = get_vacancies(secret_key=superjob_secret_key)
    print('\n'.join(vacancies))
