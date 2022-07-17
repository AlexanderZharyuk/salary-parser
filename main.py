from superjob import parse_superjob_vacancies
from hh import parse_hh_vacancies
from general_functions import create_table, get_superjob_secret_key


def main() -> None:
    superjob_secret_key = get_superjob_secret_key()
    superjob_table_title = 'SuperJob Moscow'
    superjob_vacancies = parse_superjob_vacancies(
        secret_key=superjob_secret_key
    )

    hh_table_title = 'HeadHunter Moscow'
    hh_vacancies = parse_hh_vacancies()

    print(create_table(vacancies=superjob_vacancies,
                       table_title=superjob_table_title))
    print(create_table(vacancies=hh_vacancies, table_title=hh_table_title))


if __name__ == '__main__':
    main()


