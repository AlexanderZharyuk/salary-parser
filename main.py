from superjob import parse_superjob_vacancies
from hh import parse_hh_vacancies
from table import show_table


if __name__ == '__main__':
    superjob_table_title = 'SuperJob Moscow'
    superjob_vacancies = parse_superjob_vacancies()

    hh_table_title = 'HeadHunter Moscow'
    hh_vacancies = parse_hh_vacancies()

    show_table(vacancies=superjob_vacancies, table_title=superjob_table_title)
    show_table(vacancies=hh_vacancies, table_title=hh_table_title)


