import psycopg2

def connection_postgres():
    # Replace these variables with your database connection information
    db_host = "localhost"
    db_name = "msbd"
    db_user = "postgres"
    db_password = "mypassword"
    db_port = 5432

    # Connect to the database
    try:
        connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password, port=db_port)
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL:", error)
        return None