import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

def create_database(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        print(f"Database '{db_name}' created successfully!")
    except Error as e:
        print(f"Error: '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def load_data_to_db(df, db_name, table_name, host_name, user_name, user_password):
    try:
        engine = create_engine(f"mysql+mysqlconnector://{user_name}:{user_password}@{host_name}/{db_name}")
        
        # store df into database
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f"DataFrame loaded into table '{table_name}' in database '{db_name}' successfully!")
    except Error as e:
        print(f"Error: '{e}' occurred")

