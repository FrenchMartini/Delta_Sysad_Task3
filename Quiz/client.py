import socket

def register(client_socket, username, password):

    msg= f"register,{username},{password}"
    client_socket.send(msg.encode('utf-8'))
    response=client_socket.recv(1024).decode('utf-8')
    return response


def login(client_socket, username, password):
    
    msg = f"login,{username},{password}"
    client_socket.send(msg.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    return response
    

def add_question(client_socket, username, password):
    question_text = input("Enter question: ")
    correct_answer = input("Enter correct answer: ")
    msg = f"add_question,{username},{password},{question_text},{correct_answer}"
    client_socket.send(msg.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(response)


def answer_question(client_socket, username, password):
    try : 
        client_socket.send(f"view_questions,{username},{password}".encode('utf-8'))
        questions = client_socket.recv(4096).decode('utf-8')
        print(questions)
        question_id = input("Enter the question_id which you want to answer: ")
        answer_text = input("Enter your answer: ")
        msg = f"answer_question,{username},{password},{question_id},{answer_text}"
        client_socket.send(msg.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
    except Exception as e:
        print(f"Error in answer_question: {e}")


def view_questions(client_socket, username, password):
    msg = f"view_questions,{username},{password}"
    client_socket.send(msg.encode('utf-8'))
    response = client_socket.recv(4096).decode('utf-8')
    print(response)

def view_leaderboard(client_socket, username, password):
    msg = f"view_leaderboard,{username},{password}"
    client_socket.send(msg.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(response)


def main():
    

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost',12346))

    print("\nOptions:")
    print("1. Register")
    print("2. Login")
    auth_check=input("Enter the method which you want to use to authenticate\n")
    username=input("Enter your username:\n")
    password=input("Enter your password:\n")
    if auth_check =="1":

        result = register(client_socket,username,password)
        print(result)
    elif auth_check=="2":
        result = login(client_socket,username,password)
        print(result)

    print("\nPlease choose what you would like to do next :")
    print("1. Add Question")
    print("2. Answer Question")
    print("3. View Questions")
    print("4. View Leaderboard")
    print("5. Logout")
    print("6. Exit")
    choice = input("Enter your choice:\n")

    if choice == '1':
        add_question(client_socket, username, password)
    elif choice == '2':
        answer_question(client_socket, username, password)
    elif choice == '3':
        view_questions(client_socket, username, password)
    elif choice == '4':
        view_leaderboard(client_socket, username, password)

    elif choice == '6':
        client_socket.close()
            
            
    else:
        print("Invalid choice. Please try again.")



if __name__=="__main__":
    main()






