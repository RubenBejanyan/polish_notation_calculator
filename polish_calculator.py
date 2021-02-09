import datetime
from pathlib import Path

OPERATOR_PERMITTED_VALUES = {'+', '-', '*', '/', 'add', 'sub', 'mul', 'div'}
Path('.\logging').mkdir(exist_ok=True)
my_file_path = Path('.\logging\log_file.txt').resolve()


def calculate(operator: str, operand_1: int or float, operand_2: int or float):
    if operator == '+' or operator == 'add':
        return operand_1 + operand_2
    elif operator == '-' or operator == 'sub':
        return operand_1 - operand_2
    elif operator == '*' or operator == 'mul':
        return operand_1 * operand_2
    elif operator == '/' or operator == 'div':
        return operand_1 / operand_2


def str_to_list(my_input):
    my_list = my_input.split()
    for index, item in enumerate(my_list):
        if item.isdecimal():
            my_list[index] = int(item)
        elif (''.join(x for x in item if x != '.')).isdecimal() and '.' in item:
            my_list[index] = float(item)
    return my_list


def valid_input(input_list):
    if len(input_list) == 1 and is_operator(input_list[0]):
        return False
    elif len(input_list) == 2:
        return False
    elif len(input_list) > 2 and not is_operator(input_list[0]):
        return False
    for item in input_list[-2:]:
        if not is_number(item):
            return False
    for item in input_list:
        if not is_operator(item) and not is_number(item):
            return False
    return True


def is_operator(list_element):
    return list_element in OPERATOR_PERMITTED_VALUES


def is_number(list_element):
    return type(list_element) == int or type(list_element) == float


def error_logging(my_error, my_input):
    with open(my_file_path, mode='a') as my_file:
        my_file.write(f'{datetime.datetime.now()} :: ERROR :: {my_error} :: {my_input}\n')
    print(f'ERROR: {my_error}')


def info_logging(result, my_input):
    with open(my_file_path, mode='a') as my_file:
        my_file.write(f'{datetime.datetime.now()} :: INFO :: {my_input} :: {result}\n')
    print(f'Result: {result}')


def log_report():
    with open(my_file_path) as my_file:
        error_counter = my_file.read().count('ERROR')
        my_file.seek(0)
        info_counter = my_file.read().count('INFO')
        print(f'Report: INFO-{info_counter}, ERROR-{error_counter}')


def last_log():
    with open(my_file_path) as my_file:
        return my_file.readlines()[-1]


def change_last_log(old_expression, new_expression):
    with open(my_file_path, mode='r+') as my_file:
        my_lines = my_file.readlines()
        new_string = my_lines[-1].replace(str(old_expression), str(new_expression))
        my_file.seek(0)
        my_file.write(''.join(my_lines[0:-1]))
        my_file.write(new_string)


def expression_simplification(my_list):
    new_list = my_list.copy()
    operator_flag = False
    number_flag = False
    for index, item in enumerate(new_list):
        if is_operator(item):
            operator_flag = True
            number_flag = False
            my_operator = item
        else:
            if not number_flag:
                number_flag = True
                my_number = item
            else:
                if operator_flag:
                    if item == 0 and my_operator in 'div/':
                        error_logging('Zero division error', my_list)
                        break
                    else:
                        new_list[index - 1] = 'Need delete after every loop'
                        new_list[index - 2] = 'Need delete after every loop'
                        new_list[index] = calculate(my_operator, my_number, item)
                        number_flag = False
                        operator_flag = False
    while 'Need delete after every loop' in new_list:
        new_list.remove('Need delete after every loop')
    return new_list


def recursive_simplification(my_list):
    old_list = my_list.copy()
    while len(my_list) > 1:
        if valid_input(my_list):
            if my_list == expression_simplification(my_list):
                if 'Zero division error' in last_log() and str(my_list) in last_log():
                    change_last_log(my_list, old_list)
                    return None
                else:
                    error_logging('Invalid expression', old_list)
                    return None
            else:
                my_list = expression_simplification(my_list)
                continue
        else:
            error_logging('Invalid expression', old_list)
            return None
    else:
        if valid_input(my_list):
            info_logging(my_list[0], old_list)
        else:
            error_logging('Invalid expression', old_list)


my_expression = input('Expression: ')
expression_list = str_to_list(my_expression)
recursive_simplification(expression_list)
log_report()
