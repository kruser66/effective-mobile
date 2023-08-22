import os
from typing import Dict, List
from pydantic import BaseModel, ValidationError, field_validator
from phonenumbers import parse, is_valid_number


PAGINATION = 5


class PhoneBookRecord(BaseModel):
    lastname: str
    firstname: str
    middlename: str
    company: str
    company_phone: str
    phonenumber: str

    @field_validator('lastname', 'firstname', 'middlename')
    @classmethod
    def validate_is_alpha(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError('Должны быть только буквы')
        else:
            return value.title()

    @field_validator('company_phone', 'phonenumber')
    @classmethod
    def validate_phonenumber(cls, phone: str) -> str:
        if is_valid_number(parse(phone, 'RU')):
            return phone
        else:
            raise ValueError('Формат +7ХХХХХХХХХХ или 8ХХХХХХХХХХ')


def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def display_contacts(contacts: List[PhoneBookRecord], limit_on_page: int = PAGINATION) -> None:
    clear_console()
    number_of_contact = len(contacts)
    start_contact = 0
    end_contact = min(limit_on_page, number_of_contact)
    page = 0
    while start_contact < number_of_contact:
        print(f'\nСтраница: {page + 1}')
        for index, contact in enumerate(contacts[start_contact:end_contact], start=1):
            print(f'\nЗапись № {index + page*limit_on_page}'.ljust(50, '-'))
            print(f'Фамилия: {contact.lastname}')
            print(f'Имя: {contact.firstname}')
            print(f'Отчество: {contact.middlename}')
            print(f'Название организации: {contact.company}')
            print(f'Рабочий телефон: {contact.company_phone}')
            print(f'Личный телефон: {contact.phonenumber}')
        start_contact = end_contact
        end_contact += limit_on_page
        page += 1

        quit = input('\nНажмите любую клавишу чтобы продолжить вывод или "q" для возврата в меню: ')
        if quit == 'q' or start_contact > number_of_contact:
            break
    print('\nВывод списка контактов окончен!')


def add_contact(contacts: List[Dict]) -> None:
    clear_console()
    print('Добавление новой записи в справочник:')

    lastname = input('Введите фамилию: ')
    firstname = input('Введите имя: ')
    middlename = input('Введите отчество: ')
    company = input('Введите название организации: ')
    company_phone = input('Введите рабочий телефон: ')
    phonenumber = input('Введите личный телефон: ')

    try:
        contacts.append(
            PhoneBookRecord(
                lastname=lastname,
                firstname=firstname,
                middlename=middlename,
                company=company,
                company_phone=company_phone,
                phonenumber=phonenumber
            )
        )

        save_contacts(contacts)
        print('Запись успешно добавлена!')
    except ValidationError as err:
        print(err.json(indent=4, include_url=False, include_context=False))


def edit_contact(contacts: List[PhoneBookRecord]) -> None:
    '''Редактирование записи телефонной книги'''
    clear_console()

    while True:
        contact_index = int(input('\nВведите номер записи, которую хотите отредактировать: '))
        if 0 < contact_index <= len(contacts):
            contact = contacts[contact_index - 1]
            print(f'Редактируем: \n {contact}')
            break
        else:
            print('\nНеверно указан номер записи для редактирования')

    contact.lastname = input(f'Изменить фамилию ({contact.lastname}): ') or contact.lastname
    contact.firstname = input(f'Изменить имя ({contact.firstname}): ') or contact.firstname
    contact.middlename = input(f'Изменить отчество ({contact.middlename}): ') or contact.middlename
    contact.company = input(f'Изменить название организации ({contact.company}): ') or contact.company
    contact.company_phone = input(f'Введите рабочий телефон ({contact.company_phone}): ') or contact.company_phone
    contact.phonenumber = input(f'Введите личный телефон: ({contact.phonenumber})') or contact.phonenumber
    save_contacts(contacts)

    print('Запись успешно отредактирована!')


def search_contacts(contacts: List[PhoneBookRecord], type_search: str) -> None:
    clear_console()
    print('Поиск записей в справочнике:')
    search_pattern = input('Введите строку для поиска: ')
    search_results = []
    for contact in contacts:
        if type_search == '1':
            if search_pattern.lower() in contact.lastname.lower():
                search_results.append(contact)

        elif type_search == '2':
            if search_pattern.lower() in contact.company.lower():
                search_results.append(contact)

        elif type_search == '3':
            if search_pattern.lower() in str(contact).lower():
                search_results.append(contact)

    if len(search_results) > 0:
        display_contacts(search_results)
    else:
        print('По вашему запросу ничего не найдено.')


def load_contacts() -> List[PhoneBookRecord] | None:
    '''Загрузка списка телефонных номеров из текстового файла'''

    contacts = []
    fields = PhoneBookRecord.__fields__.keys()
    try:
        with open('contacts.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    contact = PhoneBookRecord(**dict(zip(fields, line.strip().split(';'))))
                    contacts.append(contact)
                except ValidationError as err:
                    print('В файле обнаружены невалидные данные')
                    print(err.json(indent=4, include_url=False, include_context=False))
    except FileNotFoundError:
        pass

    return contacts


def save_contacts(contacts: List[PhoneBookRecord]) -> None:
    '''Сохранение телефонного справочника в текстовый файл'''

    with open('contacts.txt', 'w', encoding='utf-8') as file:
        for contact in contacts:
            line = ';'.join(contact.model_dump().values())
            file.write(line + '\n')


def main():
    contacts = load_contacts()
    while True:
        clear_console()
        print('Телефонный справочник:')
        print('1 - Вывод записей')
        print('2 - Добавление записи')
        print('3 - Редактирование записи')
        print('4 - Поиск по характеристикам')
        print('0 - Выход')
        choice = input('Выберите вариант: ')
        if choice == '1':
            display_contacts(contacts)
        elif choice == '2':
            add_contact(contacts)
        elif choice == '3':
            edit_contact(contacts)
        elif choice == '4':
            clear_console()
            print('Поиск по справочнику справочник:')
            print('1 - По Фамилии')
            print('2 - По организации')
            print('3 - По всему справочнику')
            print('0 - В меню')
            choice_type_search = input('Выберите вариант: ')
            if choice_type_search == '0':
                pass
            else:
                search_contacts(contacts, choice_type_search)
        elif choice == '0':
            break
        input('\nНажмите Enter для продолжения...')


if __name__ == '__main__':
    main()
