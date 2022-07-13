from terminaltables import AsciiTable


def show_table(vacancies: dict, table_title: str) -> None:
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
    print(table.table)
