import psycopg2


def create_database(database_name: str) -> None:
    """Создание базы данных и таблиц для сохранения данных"""

    conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='12345')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    cur.close()
    conn.close()

    conn = psycopg2.connect(host='localhost', database=f'{database_name}', user='postgres', password='12345')
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers(
                    numb SERIAL,
                    employer_id INTEGER PRIMARY KEY NOT NULL,
                    emp_name VARCHAR(100),
                    emp_url TEXT
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies(
                   vacancy_id SERIAL PRIMARY KEY,
                   vac_name VARCHAR(100),
                   employer_id INTEGER REFERENCES employers(employer_id),
                   salary_from INTEGER,
                   salary_to INTEGER,
                   salary_currency VARCHAR(10),
                   city VARCHAR(50),
                   vac_url TEXT
                )
            """)
    conn.close()


def save_information(database_name: str, employers_list: list, vacancies: list) -> None:
    """Сохранение информации в таблицы из БД"""

    conn = psycopg2.connect(host='localhost', database=f'{database_name}', user='postgres', password='12345')
    with conn:
        with conn.cursor() as cur:
            for emp in employers_list:
                cur.execute("""
                    INSERT INTO employers (employer_id, emp_name, emp_url)
                    VALUES (%s, %s, %s)
                """, (emp.get('id'), emp.get('name'), emp.get('alternate_url'))
                            )

            for vac in vacancies:
                cur.execute("""
                    INSERT INTO vacancies (vac_name, employer_id, salary_from, salary_to, 
                    salary_currency, city, vac_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (vac.get('name'), vac.get('employer')['id'],
                      vac.get('salary')['from'], vac.get('salary')['to'], vac.get('salary')['currency'],
                      vac.get('area')['name'], vac.get('apply_alternate_url'))
                )
    conn.close()
