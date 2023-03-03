import hashlib
import jwt
import mysql.connector
from decouple import config

DB_HOST = config('DB_HOST')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_DATABASE = config('DB_DATABASE')
JWT_KEY = config('JWT_KEY')


def query_data(username):
    # This database data is here just for you to test, please, remember to define your own DB
    # You can test with username = admin, password = secret  
    # This DB has already a best practice: a salt value to store the passwords
    con = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        port="3306"
    )

    cursor = con.cursor()
    cursor.execute(f"SELECT salt, password, role from users where username ='{username}';")
    query = cursor.fetchone()

    return query


class Token:
    def generateToken(self, username, password):
        query = query_data(username)
        
        if len(query):  # ToDo, check what 'query' returns when there's no data, None? Empty list?
            salt = query[0]
            hashed_password_db = query[1]
            role = query[2]

            hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()

            if hashed_password == hashed_password_db:
                return jwt.encode({"role": role}, JWT_KEY, algorithm='HS256')

            return False

        return False


class Restricted:
    def access_Data(self, authorization): 
        try:
            jwt_token = authorization.replace('Bearer ', '')  # [1:]
            jwt_decoded = jwt.decode(jwt_token, JWT_KEY, algorithms='HS256')
        except Exception as e:
            print(f"JWT token could not be decoded with error {e}.")
            return False

        if 'role' in jwt_decoded:
            return True

        return False
