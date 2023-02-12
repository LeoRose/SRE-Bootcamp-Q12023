import mysql.connector
import jwt
import hashlib
from flask import abort
import logging

# Set the logging config (for debugging purposes only).
logging.basicConfig(level=logging.DEBUG)

# Let's assume we already have some ENV variables in our instance.
DB_USER = "secret"
DB_USER_PASSWORD = "jOdznoyH6swQB9sTGdLUeeSrtejWkcw"
DB_ENDPOINT = "sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com"
SECRET_KEY = "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"

def connect_to_database():
    n_retries = 5
    for retry in range(n_retries):
        try:
            connector = mysql.connector.connect(
                host=DB_ENDPOINT,
                user=DB_USER,
                password=DB_USER_PASSWORD,
                database="bootcamp_tht",
                port="3306"
            )
            return connector
        except Exception as e:
            if retry == n_retries - 1:
                raise MaxRetriesExceededError(f"Failed to connect to the database after {n_retries} attempts with error: {e}.")
            else:
                print(f"Failed to connect to the database with error: {e}. Retrying...")


def get_user_data(connector, username):
    assert connector, "Database connector not provided."
    assert username, "Username not provided."

    cursor = connector.cursor()
    query = "SELECT * FROM users where username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    cursor.close()

    return user_data


def is_valid_password(password, salt, hashed_password):
    assert password, "Password not provided."
    assert salt, "Salt for hash not provided."
    assert hashed_password, "Hashed password not provided."

    # Checks if the hashed user password matches with the one in the database.
    hash = hashlib.sha512(str(password + salt).encode()).hexdigest()
    return True if hash == hashed_password else False


def is_valid_role(connector, role):
    assert connector, "Database connector not provided."
    assert role, "Role not provided."

    cursor = connector.cursor()
    query = "SELECT * FROM users where role = %s"
    cursor.execute(query, (role,))
    role_data = cursor.fetchone()

    return True if role_data else False


class MaxRetriesExceededError(Exception):
    pass

class JWTDecodeError(Exception):
    pass

class Token:
    def generate_token(self, username, password):
        assert username, "Username not provided."
        assert password, "Password not provided."

        connector = connect_to_database()

        # list user_data: [username, hashed_password, salt, user_role].
        user_data = get_user_data(connector, username)
        connector.close()  # Closes the connection to the DB.
        if not user_data:
            print(f"Username does not exist.")
            abort(403)

        hashed_password = user_data[1]
        salt = user_data[2]
        user_role = user_data[3]

        if is_valid_password(password, salt, hashed_password):
            return jwt.encode({"role": user_role}, SECRET_KEY)
        else:
            print(f"Incorrect password.")
            abort(403)


class Restricted:
    def access_data(self, authorization):
        assert authorization, "Authorization token not provided."

        # Decodes the token using the secret key and gets the role in the payload.
        try:
            role = jwt.decode(authorization, SECRET_KEY, algorithms=['HS256'])["role"]
        except Exception as e:
            print(f"JWT token could not be decoded with error {e}.")
            raise JWTDecodeError(f"JWT token could not be decoded with error {e}.")

        connector = connect_to_database()

        if is_valid_role(connector, role):
            return "You are under protected data"
        else:
            print(f"Role does not exist in the database.")
            abort(403)
