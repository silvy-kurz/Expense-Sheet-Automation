from typing import Dict, List
from excel import dict_categories_to_excel_single_sheet
from json_data import read_dict_from_json, write_dict_to_json
from user_input import (
    gain_user_input,
    inquire_for_starting_category,
    determine_if_date_format,
    determine_if_just_numbers,
    determine_if_just_string,
)


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
