import requests


class HeadHunterAPI:
    """Класс для работы с платформой hh.ru"""

    def __init__(self) -> None:
        """Конструктор для класса"""
        self.vac_url = []
        self.emp_url = "https://api.hh.ru/employers"
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params_vac = {'text': '', 'page': 0, 'per_page': 100,
                           'only_with_salary': True}
        self.params_emp = {'text': '', 'page': 0, 'per_page': 100,
                           'only_with_vacancies': True, 'sort_by': 'by_vacancies_open'}
        self.employers_list = []
        self.vacancies = []

    def load_employers(self, emp_list: list) -> None:
        for emp in emp_list:
            self.params_emp['text'] = emp
            emp_response = requests.get(self.emp_url, headers=self.headers, params=self.params_emp)
            employers = emp_response.json().get('items')[0]['vacancies_url']
            self.vac_url.append(employers)
            self.employers_list.append(emp_response.json()['items'][0])

    def load_vacancies(self) -> None:
        """Метод для подключения через API к HH и получение вакансий"""
        for vac_url in self.vac_url:
            self.params_vac['page'] = 0
            while self.params_vac['page'] != 20:
                response = requests.get(vac_url, headers=self.headers, params=self.params_vac)
                vacan = response.json()['items']
                self.vacancies.extend(vacan)
                self.params_vac['page'] += 1
