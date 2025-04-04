from random import randint
import re

from db import (
    init_db,
    add_to_db,
    get_filed_names,
    get_field_numbers,
    get_messages,
)

init_db()


message_pattern = r"№\d+\w*\d*\s+[А-Я][а-я]+"

template_message = "№21 Давыдовская тестовое сообщение"
while True:
    command = input()
    if command == "1":
        for i in range(1, 20):
            message = template_message + str(i)
            match = re.search(message_pattern, message)
            if match:
                part_to_remove = match.group(0)
                message_without_part = message.replace(part_to_remove, "").strip()
                (
                    field_number,
                    filed_name,
                ) = part_to_remove.split()
                field_number = field_number + str(randint(1, 9))
                add_to_db(filed_name, field_number, message_without_part)
    elif command == "2":
        field_names = list(get_filed_names())
        print(", ".join(field_names))
        selected_field_name_index = int(input())
        selected_field_name = field_names[selected_field_name_index - 1]
        print(selected_field_name)
        field_numbers = list(get_field_numbers(selected_field_name))
        print(", ".join(field_numbers))
        selected_field_number_index = int(input())
        selected_field_number = field_numbers[selected_field_number_index - 1]
        print(selected_field_number)
        # print(get_messages(selected_field_name, selected_field_number))
        start_date_input = input()
        end_date_input = input()
        print(
            get_messages(
                selected_field_name,
                selected_field_number,
                start_date_input,
                end_date_input,
            )
        )
    elif command == "0":
        break
