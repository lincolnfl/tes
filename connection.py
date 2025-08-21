import mysql.connector

def create_connection():
    host = 'mysql'
    user = 'root'
    password = 'mypassword'
    database = 'msbd'
    port = 3306

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error while connecting to MySQL: {error}")
        return None
