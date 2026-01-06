import pickle
from datetime import datetime
from typing import Dict, List
from pickle import dumps
from edwh_uuid7 import uuid7, uuid7_to_datetime
import lmdb

lmdb_path = "expenses_database"
map_size = 10 * 1024 * 1024 * 1024  # 1 GB
env = lmdb.open(lmdb_path, map_size=map_size)


def create_unique_expense_identifier() -> str:
    random_sequential_uuid7 = str(uuid7())
    return random_sequential_uuid7


def add_expense_to_database(database, expense: Dict[str, str]) -> None:
    expense_date = expense["Date"]
    database_key = f"{expense_date}_{create_unique_expense_identifier()}"

    key_bytes = database_key.encode()
    expense_bytes = dumps(expense)

    database.put(key_bytes, expense_bytes)


def read_expense_from_database(database, database_key):
    expense_bytes = database.get(database_key)
    expense = pickle.loads(expense_bytes)

    return expense


def extract_current_year():
    current_datetime = datetime.now()

    return current_datetime.year


def build_dict_from_database_section(database_cursor, section_condition):
    all_keys = database_cursor.keys()
    section_keys = filter(section_condition, all_keys)
    print(section_keys)


def show_all_database():
    with env.begin() as txn:
        # Get a cursor
        print("dasjjkasdjks")
        with txn.cursor() as curs:
            for key, value in curs:
                expense = pickle.loads(value)
                print(key.decode("utf-8"))
                print(expense)


if __name__ == "__main__":
    # testing_expense = {
    #     "Item": "red brown teal pants plus Jordan",
    #     "Amount": "3000",
    #     "Date": "2025-29-12",
    # }

    # with env.begin(write=True) as database:
    #     add_expense_to_database(database, testing_expense)

    show_all_database()
    with env.begin() as txn:
        # Get a cursor
        print("dasjjkasdjks")
        with txn.cursor() as curs:
            build_dict_from_database_section(curs, lambda x: b"5" in x)
