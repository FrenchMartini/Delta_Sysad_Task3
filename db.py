import psycopg2 #helps us to interact with the db =

# Database connection setup
conn = psycopg2.connect(
    database="task3",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create users table
def users_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(255) 
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()

# Run the table creation functions
if __name__ == "__main__":
    users_table()
    print("Users table created successfully")

# Close the database connection
cursor.close()
conn.close()