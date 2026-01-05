def print_out_category_rows(
    column_size: int, category_list: list[str], column: int
) -> None:
    print("    ", end="")
    for item in category_list[
        column * column_size : column * column_size + column_size
    ]:
        space = "                "[0 : 16 - len(item)]
        print(item + space, end="")
    print("    \n")

    print("    ", end="")
    for item in category_list[
        column * column_size : column * column_size + column_size
    ]:
        shortened_item = f"({item[0:2]})"
        space = "                "[0 : 16 - (len(shortened_item))]

        print(shortened_item + space, end="")
    print("    \n")


def gain_user_input(question, additional_boolean_funciton):
    user_input = input(f"{question}: ")
    while user_input == "" or not additional_boolean_funciton(user_input):
        user_input = input(f"{question}: ")

    return user_input


def determine_if_just_string(item: str) -> bool:
    return all(character.isalpha() or character.isspace() for character in item)


def determine_if_just_numbers(item: str) -> bool:
    while "." in item:
        item = item[0 : item.index(".")] + item[item.index(".") + 1 :]
        print(item)
    while "," in item:
        item = item[0 : item.index(",")] + item[item.index(",") + 1 :]

    return item.isnumeric()


def determine_if_date_format(item: str) -> bool:
    if item[0:2].isnumeric() and item[2] == "-" and item[3:5].isnumeric():
        return int(item[3:5]) <= 12
    return False


def inquire_for_starting_category(category_list) -> str:
    column_size: int = 4
    row_number: int = (len(category_list) + column_size - 1) // column_size
    print("    ")
    print("    ")

    print(
        "Here Are All the Categories you have for Expense Items and their Abbreviations:"
    )
    print("    ")

    abbreviation_category_conversion: dict[str, str] = {
        category[0:2]: category for category in category_list
    }
    for row in range(row_number):
        print_out_category_rows(column_size, category_list, row)
    abbreviated_category: str = input(
        "Please Type the Abbreviation for the Categories: "
    ).upper()
    while abbreviated_category not in list(abbreviation_category_conversion):
        abbreviated_category: str = input(
            "Please Type the Abbreviation for the Categories: "
        ).upper()

    return abbreviation_category_conversion[abbreviated_category]
