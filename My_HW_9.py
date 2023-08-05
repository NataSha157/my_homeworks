"""
Напишіть консольного бота помічника, який розпізнаватиме команди, що вводяться з клавіатури, і відповідати відповідно до
введеної команди.

Бот помічник повинен стати для нас прототипом застосунку-асистента. Застосунок-асистент в першому наближенні повинен
вміти працювати з книгою контактів і календарем. У цій домашній роботі зосередимося на інтерфейсі самого бота.
Найпростіший і найзручніший на початковому етапі розробки інтерфейс - це консольний застосунок CLI
(Command Line Interface). CLI достатньо просто реалізувати. Будь-який CLI складається з трьох основних елементів:

Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, виділення з рядка ключових слів та
модифікаторів команд.
Функції обробники команд — набір функцій, які ще називають handler, вони відповідають за безпосереднє виконання команд.
Цикл запит-відповідь. Ця частина застосунку відповідає за отримання від користувача даних та повернення користувачеві
відповіді від функції-handlerа.
На першому етапі наш бот-асистент повинен вміти зберігати ім'я та номер телефону, знаходити номер телефону за ім'ям,
змінювати записаний номер телефону, виводити в консоль всі записи, які зберіг. Щоб реалізувати таку нескладну логіку,
скористаємося словником. У словнику будемо зберігати ім'я користувача як ключ і номер телефону як значення.

Умови
Бот повинен перебувати в нескінченному циклі, чекаючи команди користувача.
Бот завершує свою роботу, якщо зустрічає слова: "good bye", "close", "exit".
Бот не чутливий до регістру введених команд.
Бот приймає команди:
"hello", відповідає у консоль "How can I help you?"
"add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад) новий контакт. Замість ... користувач вводить
ім'я та номер телефону, обов'язково через пробіл.
"change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту. Замість ... користувач
вводить ім'я та номер телефону, обов'язково через пробіл.
"phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту. Замість ... користувач
вводить ім'я контакту, чий номер потрібно показати.
"show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
"good bye", "close", "exit" за будь-якою з цих команд бот завершує свою роботу після того, як виведе у консоль "Good bye!".
Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. Цей декоратор відповідає за
повернення користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо. Декоратор input_error
повинен обробляти винятки, що виникають у функціях-handler (KeyError, ValueError, IndexError) та повертати відповідну
відповідь користувачеві.
Логіка команд реалізована в окремих функціях і ці функції приймають на вхід один або декілька рядків та повертають рядок.
Вся логіка взаємодії з користувачем реалізована у функції main, всі print та input відбуваються тільки там.
"""

MY_ADRESSBOOK = {}

# COMMAND_PREFIXES = ("hello", "add", "change", "phone", "show all", "good bye", "close", "exit")

def input_error(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Give me name and phone please"
        except KeyError:
            return "This name does not exist in contacts"
        except ValueError:
            return "Enter a valid value"
    return wrap



# Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, виділення з рядка ключових слів та модифікаторів команд.

@input_error
def commands_parser(string: str):
    work_list = string.lower().split(' ')
    for func, command in COMMANDS_HANDLER.items():
        for cmd in command:
            if cmd.startswith(work_list[0]):
                return func(work_list[1:])
    return "Unknown command"



# @input_error
# def parser_str(string: str):
#     work_list = string.lower().split(' ')
#     if work_list[0] == "hello":
#         return hello_handler()
#     elif work_list[0] == "add":
#         return add_handler(work_list[1:])
#     elif work_list[0] == "change":
#         return change_handler(work_list[1:])
#     elif work_list[0] == "phone":
#         return phone_handler(work_list[1:])
#     elif work_list[0] == "show" and work_list[1] == "all":
#         return show_handler()
#     elif work_list[0] == "close" or work_list[0] == "exit" or (work_list[0] == "good" and work_list[1] == "bye"):
#         return good_bye_handler()





# Функції обробники команд — набір функцій, які ще називають handler, вони відповідають за безпосереднє виконання команд.
#@input_error
def hello_handler(*args, **kwargs):
    return "How can I help you?"



#@input_error
def add_handler(contact: list):
    new_user = str(contact[0]).title()
    new_phone = contact[1]
    MY_ADRESSBOOK[new_user] = new_phone
    return f"Contact {new_user} with phone {new_phone} was saved."

#@input_error
def change_handler(contact: list):
    old_user = str(contact[0]).title()
    new_phone = contact[1]
    MY_ADRESSBOOK[old_user] = new_phone
    return f"Contact {old_user} changed his phone. New phone: {new_phone}."

@input_error
def phone_handler(contact: list):
    old_user = str(contact[0]).title()
    old_phone = MY_ADRESSBOOK.get(old_user)
    return f"Contact {old_user} have a phone number: {old_phone}."


#@input_error
def show_handler(*args, **kwargs): # Тут треба компрехеншн словника
    res = ''
    for contact, phone in MY_ADRESSBOOK.items():
        res += f"Contact {contact} have a phone number: {phone}. \n"
    return res


@input_error
def good_bye_handler(*args, **kwargs):
    return "Good bye!"




# Цикл запит-відповідь. Ця частина застосунку відповідає за отримання від користувача даних та повернення користувачеві відповіді від функції-handlerа.


COMMANDS_HANDLER = {
    hello_handler: ["hello"],
    add_handler: ["add"],
    change_handler: ["change"],
    phone_handler: ["phone"],
    show_handler: ["show all"],
    good_bye_handler: ["good bye", "close", "exit"]
}

def main():
    print('Hello! I am your bot-helper. I can help you to create your contact-book. I am ready and wait you command. ')
    while True:
        human_command = input('>>>  ')
        result = commands_parser(human_command)
        print(result)
        if result == good_bye_handler():
            break

        # func = parser_str(human_command)
        # print(func)
        # if func == good_bye_handler():
        #     break



if __name__ == '__main__':
    main()