import socket
import psycopg2
import threading 

# Database connection setup
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)
cursor = conn.cursor()

def handle_client(client_socket):
    try:
        while True:     
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print("no data receieved ,closing connection")
                break;
            print("Received data:", data)
            response = process_data(data)
            print("Sending response:", response)
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

def process_data(data):
    parts = data.split(',')
    if len(parts) < 3:
        print("Invalid data format")
        return "Invalid data format"
    
    action = parts[0]
    username = parts[1]
    password = parts[2]

    print(f"Action: {action}, Username: {username}, Password: {password}")
    action = parts[0]
    username = parts[1]
    password = parts[2]

    if action == "register":
        return register_user(username, password)
    elif action == "login":
        return login_user(username, password)
    elif action == "add_question":
        question_text = parts[3]
        correct_answer = parts[4]
        return add_question(username, question_text, correct_answer)
    elif action == "answer_question":
        question_id = parts[3]
        answer_text = parts[4]
        return answer_question(username, question_id, answer_text)
    elif action == "view_questions":
        return view_questions()
    elif action == "view_leaderboard":
        return view_leaderboard()
    else:
        return "Unknown Action"


#using this function to register new users upon client action and inserting detalis into db
def register_user(username, password):
    try:
        print(f"Registering user: {username}")

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return "Registration successful"
    except psycopg2.IntegrityError:
        conn.rollback()
        return "Username already exists"
    
#login func to check if user already exists in db 
def login_user(username, password):
        print(f"Logging in user: {username}")
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",(username, password))
        result = cursor.fetchone()

        #Returns true if user is found 
        if result is not None:
            if  result[1]== password and result[0] == username:
                return "Login succesful "
            else:
                return "Incorrect loggin Credentials"
        else:
            return "No user found"
        
def add_question(username, question_text, correct_answer):
    try:
        cursor.execute("INSERT INTO questions (username, question_text, correct_answer) VALUES (%s, %s, %s)", (username,question_text,correct_answer))
        conn.commit()
        return "Question added successfully"
    except:
        conn.rollback()
        return "Error adding question"

def answer_question(username, question_id, answer_text):
    try:
        cursor.execute("SELECT username, correct_answer FROM questions WHERE id = %s", (question_id,))
        question = cursor.fetchone()

        if question and question[0] != username:
            correct_answer = question[1]
            if answer_text.lower() == correct_answer.lower():
                cursor.execute("UPDATE questions SET answer = %s WHERE id = %s", (answer_text, question_id))
                conn.commit()
                cursor.execute("INSERT INTO leaderboard (username, points) VALUES (%s, 1) ON CONFLICT (username) DO UPDATE SET points = leaderboard.points + 1", (username,))
                conn.commit()
            
                return "Answer submitted and correct!"
            else:
                
                return "Answer submitted but incorrect."
        else:
            
                return "You cannot answer your own question or question not found"
    except:
        conn.rollback()
        return "Error answering question"


def view_questions():
    cursor.execute("SELECT id, question_text, username FROM questions WHERE answer IS NULL")
    questions = cursor.fetchall()
    print("Sending questions:\n", questions)  # Debugging print

    if not questions:
        return "No questions available"
    return "\n".join(f"{q[0]}. {q[1]} (by {q[2]})" for q in questions)

def view_leaderboard():
    cursor.execute("SELECT username, points FROM leaderboard ORDER BY points DESC")
    leaderboard = cursor.fetchall()
    if not leaderboard:
        return "Leaderboard is empty"
    return "\n".join(f"{username}: {points} points" for username, points in leaderboard)


def main():
    print("Starting server .....")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12346))
    server_socket.listen(5)
    print("Server is listening on port 12345")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()