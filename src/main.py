from src.function import *
from src.dbmanager_class import *
from src.hh_class import *


def main():
    """Функция запускающее приложение"""
    print("Здравствуйте! Программа осуществляет поиск вакансий среди следующих компаний:\n"
          "Яндекс, Сбербанк, Газпром, Лукойл, РЖД , Роснефть, Россети, Мегафон, Согаз\n"
          "Дождитесь окончание поиска и создания базы данных. Это займет некоторое время.")
    hh = HeadHunterAPI()
    params_emp = ["Яндекс", "Сбербанк", "Газпром", "Лукойл",
                  "РЖД", "Роснефть", "Россети", "Мегафон", "Согаз"]
    hh.load_employers(params_emp)
    hh.load_vacancies()
    create_database('skypro')
    save_information('skypro', hh.employers_list, hh.vacancies)
    db = DBManager()
    print("Создана база данных 'skypro' c таблицами 'employers' и 'vacancies'")
    db.repeating_actions()


if __name__ == '__main__':
    main()
