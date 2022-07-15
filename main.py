from superjob import parse_superjob_vacancies
from hh import parse_hh_vacancies
from general_functions import show_table, get_superjob_secret_key


if __name__ == '__main__':
    superjob_secret_key = get_superjob_secret_key()
    superjob_table_title = 'SuperJob Moscow'
    superjob_vacancies = parse_superjob_vacancies(
        secret_key=superjob_secret_key
    )

    hh_table_title = 'HeadHunter Moscow'
    hh_vacancies = parse_hh_vacancies()

    show_table(vacancies=superjob_vacancies, table_title=superjob_table_title)
    show_table(vacancies=hh_vacancies, table_title=hh_table_title)


