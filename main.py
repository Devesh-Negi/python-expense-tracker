
from datetime import date
from decimal import Decimal, InvalidOperation

import mysql.connector
from db import get_connection


def add_expense():
    try:
        amount = Decimal(input("Enter amount: ").strip())

        if not amount.is_finite() or amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount.as_tuple().exponent < -2:
            print("Amount can have at most two decimal places.")
            return

        category = input("Enter category: ").strip()
        description = input("Enter description: ").strip()

        if not category:
            print("Category cannot be empty.")
            return

        if len(category) > 50 or len(description) > 255:
            print("Category or description is too long.")
            return

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO expenses
                (amount, category, description, expense_date)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            amount,
            category,
            description or None,
            date.today(),
        )

        cursor.execute(query, values)
        connection.commit()

        print("Expense added successfully!")

    except (InvalidOperation, ValueError):
        print("Please enter a valid amount.")
    except mysql.connector.Error as error:
        print("Database error:", error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()

def view_expenses():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT id, amount, category, description, expense_date
            FROM expenses
            ORDER BY expense_date DESC, id DESC
        """

        cursor.execute(query)
        expenses = cursor.fetchall()

        if not expenses:
            print("No expenses found.")
            return

        print("\n--- All Expenses ---")
        print("ID | Amount | Category | Description | Date")
        print("-" * 60)

        for expense in expenses:
            print(" | ".join(str(value or "") for value in expense))

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def show_total():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "SELECT COALESCE(SUM(amount), 0) FROM expenses"
        cursor.execute(query)

        total = cursor.fetchone()[0]

        print(f"\nTotal expenses: Rs. {total:.2f}")

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def search_by_category():
    category = input("Enter category to search: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT id, amount, category, description, expense_date
            FROM expenses
            WHERE category = %s
            ORDER BY expense_date DESC
        """

        cursor.execute(query, (category,))
        expenses = cursor.fetchall()

        if not expenses:
            print("No expenses found in this category.")
            return

        print("\n--- Search Results ---")

        for expense in expenses:
            print(" | ".join(str(value or "") for value in expense))

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def delete_expense():
    try:
        expense_id = int(input("Enter expense ID to delete: "))

        if expense_id <= 0:
            print("ID must be a positive number.")
            return

    except ValueError:
        print("Please enter a valid integer ID.")
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "DELETE FROM expenses WHERE id = %s"
        cursor.execute(query, (expense_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print("Expense deleted successfully!")
        else:
            print("No expense found with that ID.")

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()



def main():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Expenses")
        print("4. Search by Category")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total()
        elif choice == "4":
            search_by_category()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Show Total Expenses")
    print("4. Search by Category")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        show_total()
    elif choice == "4":
        search_by_category()
    else:
        print("Invalid choice.")
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Show Total Expenses")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        show_total()
    else:
        print("Invalid choice.")
    print("1. Add Expense")
    print("2. View Expenses")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    else:
        print("Invalid choice.")