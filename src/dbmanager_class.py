import psycopg2


class DBManager:
    """класс для подключения к БД и работы с ней"""

    @staticmethod
    def get_companies_and_vacancies_count():
        """Получает список всех компаний и количество вакансий у
        каждой компании."""
        conn = psycopg2.connect(host='localhost', database=f'skypro', user='postgres', password='12345')
        with conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT emp_name, COUNT(vac_name) as vacancy_count 
        FROM employers 
        INNER JOIN vacancies ON employers.employer_id = vacancies.employer_id 
        GROUP BY emp_name 
        ORDER BY vacancy_count DESC""")
                rows = cur.fetchall()
                for row in rows:
                    print(f'Компания: {row[0]}, количество вакансий - {row[1]} шт.')
        conn.close()

    @staticmethod
    def get_all_vacancies():
        """Получает список всех вакансий с указанием
        названия компании, названия вакансии и зарплаты и ссылки
        на вакансию."""
        conn = psycopg2.connect(host='localhost', database=f'skypro', user='postgres', password='12345')
        with conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT
        emp_name, vac_name, salary_from, salary_to, salary_currency, vac_url
        FROM employers
        INNER JOIN vacancies ON employers.employer_id = vacancies.employer_id""")
                rows = cur.fetchall()
                for row in rows:
                    print(f'Компания: {row[0]}, {row[1]}, зарплата: {row[2]} - {row[3]} {row[4]}, '
                          f'ссылка на вакансию: {row[5]}')
        conn.close()

    @staticmethod
    def get_avg_salary():
        """Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(host='localhost', database=f'skypro', user='postgres', password='12345')
        with conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT AVG(salary_from), AVG(salary_to)
        FROM vacancies
        WHERE salary_currency = 'RUR'""")
                rows = cur.fetchall()
                for row in rows:
                    print(f' Средняя зарплата от {round(row[0])} руб. до {round(row[1])} руб.')

        conn.close()

    @staticmethod
    def get_vacancies_with_higher_salary():
        """Получает список всех вакансий, у которых зарплата
        выше средней по всем вакансиям."""
        conn = psycopg2.connect(host='localhost', database=f'skypro', user='postgres', password='12345')
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT emp_name, vac_name, salary_from, salary_to, vac_url
                FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE salary_from > ANY(SELECT AVG(salary_from) FROM vacancies) AND 
                salary_to > ANY(SELECT AVG(salary_to) FROM vacancies) AND salary_currency = 'RUR' 
                ORDER BY salary_from""")
                rows = cur.fetchall()
                for row in rows:
                    print(f'Компания: {row[0]}, {row[1]}, зарплата: {row[2]} - {row[3]} руб., '
                          f'ссылка на вакансию: {row[4]}')

        conn.close()

    @staticmethod
    def get_vacancies_with_keyword(user_input: str):
        """Получает список всех вакансий, в названии
        которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(host='localhost', database=f'skypro', user='postgres', password='12345')
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT emp_name, vac_name, salary_from, salary_to, salary_currency, vac_url
            FROM employers
            INNER JOIN vacancies ON employers.employer_id = vacancies.employer_id
            WHERE vac_name LIKE '%{user_input}%'""")
                rows = cur.fetchall()
                for row in rows:
                    print(f'Компания: {row[0]}, {row[1]}, зарплата: {row[2]} - {row[3]} {row[4]}, '
                          f'ссылка на вакансию: {row[5]}')

        conn.close()

    def repeating_actions(self):
        """Функция для создания цикла в программе"""

        massage = ("\nДля работы с базой данных для Вас доступны следующие функции:\n"
                   "Введите '1' для  получения всех компаний и количество вакансий у каждой компании.\n"
                   "Введите '2' для  получения всех вакансий с указанием названия компании, "
                   "названия вакансии и зарплаты и ссылки на вакансию.\n"
                   "Введите '3' для  получения средней зарплаты по вакансиям.\n"
                   "Введите '4' для  получения всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                   "Введите '5' для  поиска вакансии по заданному слову.\n"
                   "Введите '0' для  выхода из программы.\n")
        while True:
            print(massage)
            user_input = input("Введите цифру: ")
            if int(user_input) == 0:
                break
            elif int(user_input) == 1:
                self.get_companies_and_vacancies_count()
            elif int(user_input) == 2:
                self.get_all_vacancies()
            elif int(user_input) == 3:
                self.get_avg_salary()
            elif int(user_input) == 4:
                self.get_vacancies_with_higher_salary()
            elif int(user_input) == 5:
                self.get_vacancies_with_keyword(str(input("Введите слово для поиска: ")))
            else:
                print("Извините но данная команда отсутствует")
        print("Работа программы завершена!")
