from datetime import datetime, timedelta
from random import randint
import sqlite3


def init_db():
    with sqlite3.connect("sqlite_project/my_database.db") as connection:
        connection = sqlite3.connect("sqlite_project/my_database.db")
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_name TEXT NOT NULL,
            field_number TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP
            )
            """
        )
        connection.commit()


def add_to_db(field_name, field_number, message):
    with sqlite3.connect("sqlite_project/my_database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO messages (field_name, field_number, message, timestamp) VALUES (?, ?, ?, ?)",
            (
                field_name,
                field_number,
                message,
                datetime.now()),
            ),
        )
        connection.commit()


def get_filed_names():
    with sqlite3.connect("sqlite_project/my_database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT field_name from messages")
        fields = set([i[0] for i in cursor.fetchall()])
    return fields


def get_field_numbers(field_name):
    with sqlite3.connect("sqlite_project/my_database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT field_number from messages WHERE field_name = ?", (field_name,)
        )
        field_numbers = set([i[0] for i in cursor.fetchall()])
    return field_numbers


def get_messages(field_name, field_number, start_date="", end_date=""):
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%d.%m.%Y").date()
        except ValueError:
            print("Некорректная начальная дата")
            return
    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%d.%m.%Y").date()
        except ValueError:
            print("Некорректная конечная дата")
            return
    if start_date and end_date and start_date >= end_date:
        print("Начальная дата должна быть раньше конечной даты.")
        return
    with sqlite3.connect("sqlite_project/my_database.db") as connection:
        cursor = connection.cursor()
        if start_date and end_date:
            cursor.execute(
                "SELECT message FROM messages WHERE field_name = ? AND field_number = ? and timestamp BETWEEN ? AND ?",
                (field_name, field_number, start_date, end_date),
            )
        elif start_date:
            cursor.execute(
                "SELECT message FROM messages WHERE field_name = ? AND field_number = ? and timestamp >= ?",
                (
                    field_name,
                    field_number,
                    start_date,
                ),
            )
        elif end_date:
            cursor.execute(
                "SELECT message FROM messages WHERE field_name = ? AND field_number = ? and timestamp <= ?",
                (
                    field_name,
                    field_number,
                    end_date,
                ),
            )
        else:
            cursor.execute(
                "SELECT message FROM messages WHERE field_name = ? AND field_number = ?",
                (field_name, field_number),
            )
        messages = [i[0] for i in cursor.fetchall()]
    return messages
