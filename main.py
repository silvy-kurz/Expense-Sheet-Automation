from typing import Dict, List
from utils import (
    dict_categories_to_excel_single_sheet,
    read_dict_from_json,
    write_dict_to_json,
    determine_if_date_format,
    determine_if_just_numbers,
    determine_if_just_string,
)


def gain_user_input(question, additional_boolean_funciton=lambda x: True):
    user_input = input(f"{question}: ")
    while user_input == "" or not additional_boolean_funciton(user_input):
        user_input = input(f"{question}: ")

    return user_input


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


def add_expense_item() -> dict[str, str | int]:
    Item = gain_user_input("Item", additional_boolean_funciton=determine_if_just_string)

    Amount = gain_user_input(
        "Amount", additional_boolean_funciton=determine_if_just_numbers
    )
    Date = gain_user_input(
        "Date (DD-MM)", additional_boolean_funciton=determine_if_date_format
    )
    print(Date)

    return {"Item": Item, "Amount": Amount, "Date": Date}


def add_totals(
    expense_dict: Dict[str, List[Dict[str, str | int]]],
) -> Dict[str, List[Dict[str, str | int]]]:
    all_categories_total = 0
    for category in expense_dict:
        print(category)
        category_sub_total = 0
        expense_dict[category].append({"Item": "SUBTOTAL", "Amount": 0})

        for expense_item in expense_dict[category]:
            if not expense_item["Item"] == "SUBTOTAL":
                print(int(expense_item["Amount"]))
                category_sub_total += int(expense_item["Amount"])
            else:
                expense_item["Amount"] = category_sub_total
                all_categories_total += category_sub_total
        print("==========")
    expense_dict[""] = [{"TOTAL FOR ALL CATEGORIES": all_categories_total}]
    return expense_dict


def main():
    print("dingus")
    # category_list: list[str] = ["GROCERIES", "RESTAURANTS", "CLOTHING", "TRIPS", "PHARMACY", "FITNESS", "HOUSEHOLD", "GIFTS", "MASSAGE/HAIR", "TIPS",  "JEWELLERY", "CAT", "TAILOR", "MISCELEANOUS"]
    expenses_dictionary: Dict[str, List[Dict[str, str | int]]] = read_dict_from_json(
        "expenses.json"
    )
    category_list = list(expenses_dictionary)

    # for i in category_list:
    #     if not i in list(expenses_dictionary):
    #         expenses_dictionary[i] = []

    continuation_input: str = ""
    question_to_gauge_continuation = "Would you like to Stop Inputting Items? Type (Y) if you would like to stop the program, (C) if you would like to switch category, (D) if you would like to delete your previous item, and return without pressing any keys if you would like to keep inputting items: "
    category = inquire_for_starting_category(category_list)

    while "Y" not in continuation_input:
        # while False:
        expenses_dictionary[category].append(add_expense_item())
        print("===")
        print("===")
        continuation_input = input(question_to_gauge_continuation).upper()
        while (
            continuation_input != "D"
            and continuation_input != "C"
            and continuation_input != "Y"
            and continuation_input != ""
        ):
            continuation_input = input(question_to_gauge_continuation).upper()
        if continuation_input == "C":
            category = inquire_for_starting_category(category_list)

        if continuation_input == "D":
            expenses_dictionary[category].pop(-1)
            continuation_input = inquire_for_starting_category(category_list)
    print(expenses_dictionary)
    write_dict_to_json(expenses_dictionary, "expenses.json")
    expenses_dictionary = add_totals(expenses_dictionary)
    dict_categories_to_excel_single_sheet(expenses_dictionary, "expenses.xlsx")


if __name__ == "__main__":
    main()
