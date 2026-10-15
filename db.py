
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "expense_tracker"),
    )
    return connection


if __name__ == "__main__":
    connection = None

    try:
        connection = get_connection()
        print("MySQL connected successfully!")
    except mysql.connector.Error as error:
        print("Connection failed:", error)
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("Connection closed.")
