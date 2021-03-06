import os

from dotenv import load_dotenv

from terminaltables import AsciiTable


def get_superjob_secret_key() -> str:
    load_dotenv()
    return os.environ['SUPERJOB_SECRET_KEY']


def predict_salary(salary_from: int, salary_to: int) -> int | None:
    if not salary_from and not salary_to:
        return None
    elif not salary_from:
        return int(salary_to * 0.8)
    elif not salary_to:
        return int(salary_from * 1.2)

    return (salary_to + salary_from) // 2


def create_table(vacancies: dict, table_title: str) -> str:
    table_rows = [
        [
            'Язык программирования', 'Вакансий найдено',
            'Вакансий обработано', 'Средняя зарплата'
        ]
    ]

    for programming_language, statistic in vacancies.items():
        total_vacancies = statistic['vacancies_found']
        vacancies_processed = statistic['vacancies_processed']
        average_salary = statistic['average_salary']
        table_row = [
            programming_language, total_vacancies,
            vacancies_processed, average_salary
        ]
        table_rows.append(table_row)

    table = AsciiTable(table_data=table_rows, title=table_title)
    return table.table
