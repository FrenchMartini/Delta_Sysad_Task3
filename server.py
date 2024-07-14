import socket
import psycopg2

# Database connection setup
conn = psycopg2.connect(
    database="task3",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

def handle_client_request(data):
    parts = data.split(',')
    action = parts[0]

    if action == "register":
        username = parts[1]
        password = parts[2]
        return register_user(username, password)
    

def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return "Registration successful"
    except psycopg2.IntegrityError:
        conn.rollback()
        return "Username already exists"

def query_database(query_id):
    cursor.execute("SELECT * FROM your_table WHERE id = %s", (query_id,))
    result = cursor.fetchone()
    return str(result) if result else "No data found"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        
        data = client_socket.recv(1024).decode('utf-8')
        response = handle_client_request(data)
        
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

start_server()
