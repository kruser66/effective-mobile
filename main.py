import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_contacts(contacts):
    clear_console()
    for contact in contacts:
        print("-" * 50)
        print(f"Фамилия: {contact['Фамилия']}")
        print(f"Имя: {contact['Имя']}")
        print(f"Отчество: {contact['Отчество']}")
        print(f"Название организации: {contact['Название организации']}")
        print(f"Рабочий телефон: {contact['Рабочий телефон']}")
        print(f"Личный телефон: {contact['Личный телефон']}")


def add_contact(contacts):
    clear_console()
    print("Добавление новой записи в справочник:")
    contact = {}
    contact['Фамилия'] = input("Введите фамилию: ")
    contact['Имя'] = input("Введите имя: ")
    contact['Отчество'] = input("Введите отчество: ")
    contact['Название организации'] = input("Введите название организации: ")
    contact['Рабочий телефон'] = input("Введите рабочий телефон: ")
    contact['Личный телефон'] = input("Введите личный телефон: ")
    contacts.append(contact)
    save_contacts(contacts)
    print("Запись успешно добавлена!")


def edit_contact(contacts):
    clear_console()
    print("Редактирование записи в справочнике:")
    display_contacts(contacts)
    contact_index = int(input("Введите номер записи, которую хотите отредактировать: "))
    contact = contacts[contact_index]
    contact['Фамилия'] = input("Введите фамилию: ")
    contact['Имя'] = input("Введите имя: ")
    contact['Отчество'] = input("Введите отчество: ")
    contact['Название организации'] = input("Введите название организации: ")
    contact['Рабочий телефон'] = input("Введите рабочий телефон: ")
    contact['Личный телефон'] = input("Введите личный телефон: ")
    save_contacts(contacts)
    print("Запись успешно отредактирована!")


def search_contacts(contacts):
    clear_console()
    print("Поиск записей в справочнике:")
    search_term = input("Введите фамилию, имя или название организации: ")
    search_results = []
    for contact in contacts:
        if search_term.lower() in contact['Фамилия'].lower() or \
                search_term.lower() in contact['Имя'].lower() or \
                search_term.lower() in contact['Название организации'].lower():
            search_results.append(contact)
    if len(search_results) > 0:
        display_contacts(search_results)
    else:
        print("По вашему запросу ничего не найдено.")


def load_contacts():
    contacts = []
    try:
        with open("contacts.txt", "r", encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                contact_data = line.strip().split(";")
                contact = {
                    "Фамилия": contact_data[0],
                    "Имя": contact_data[1],
                    "Отчество": contact_data[2],
                    "Название организации": contact_data[3],
                    "Рабочий телефон": contact_data[4],
                    "Личный телефон": contact_data[5]
                }
                contacts.append(contact)
    except FileNotFoundError:
        pass
    return contacts


def save_contacts(contacts):
    with open("contacts.txt", "w", encoding='utf-8') as file:
        for contact in contacts:
            line = ";".join([
                contact['Фамилия'],
                contact['Имя'],
                contact['Отчество'],
                contact['Название организации'],
                contact['Рабочий телефон'],
                contact['Личный телефон']
            ])
            file.write(line + "\n")


def main():
    contacts = load_contacts()
    while True:
        clear_console()
        print("Телефонный справочник:")
        print("1 - Вывод записей")
        print("2 - Добавление записи")
        print("3 - Редактирование записи")
        print("4 - Поиск по характеристикам")
        print("0 - Выход")
        choice = input("Выберите вариант: ")
        if choice == "1":
            display_contacts(contacts)
            input("Нажмите Enter для продолжения...")
        elif choice == "2":
            add_contact(contacts)
            input("Нажмите Enter для продолжения...")
        elif choice == "3":
            edit_contact(contacts)
            input("Нажмите Enter для продолжения...")
        elif choice == "4":
            search_contacts(contacts)
            input("Нажмите Enter для продолжения...")
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
