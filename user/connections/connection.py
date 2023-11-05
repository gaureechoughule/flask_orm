import mysql.connector

# MySQL Configuration
config = {
    'user': 'root',
    'password': 'prathamesh',
    'host': 'localhost',
    'database': 'crud',
}

def get_connection():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

