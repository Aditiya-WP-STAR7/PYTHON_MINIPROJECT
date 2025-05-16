import json
import time
import os
import re
from getpass import getpass
from datetime import datetime
import random
import re
from datetime import datetime
import random

users = {}
chat_history = {}
admin_password = "admin123"

# ==== Color for CLI ====
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

# ==== AI Chatbot Core ====
def chatbot_response(message):
    message = message.lower().strip()

    # === Evaluate full math expressions securely ===
    if re.match(r'^[\d\s\.\+\-\*/]+$', message):
        try:
            result = round(eval(message), 2)
            return f"The result of '{message}' is {result}."
        except ZeroDivisionError:
            return "Division by zero is undefined."
        except:
            pass  # Not a valid math expression, fall through

    # === General conversation logic ===
    if "your name" in message:
        return "My name is PyBot, your simple AI assistant."
    elif "how old are you" in message:
        return "I'm a timeless piece of code — forever young!"
    elif "where are you from" in message:
        return "I live in the cloud, powered by Python."

    if "time" in message:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    elif "date" in message or "day" in message:
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

    if "motivate" in message or "motivation" in message:
        return random.choice([
            "Believe in yourself!",
            "Every expert was once a beginner.",
            "Mistakes are proof that you're trying.",
        ])

    if "fact" in message:
        return random.choice([
            "Did you know? Honey never spoils!",
            "The Eiffel Tower can grow taller in summer.",
            "Bananas are berries, but strawberries aren't.",
        ])

    if "quote" in message:
        return random.choice([
            "“The only true wisdom is in knowing you know nothing.” – Socrates",
            "“To be is to do.” – Immanuel Kant",
            "“Do or do not, there is no try.” – Yoda",
        ])

    if "joke" in message or "funny" in message or "laugh" in message:
        return random.choice([
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the math book look sad? Because it had too many problems.",
            "Parallel lines have so much in common… it’s a shame they’ll never meet.",
        ])

    if "hello" in message or "hi" in message or "hey" in message:
        return "Hello! How can I assist you today?"

    if "how are you" in message:
        return "I'm doing great! Just waiting to chat with you."

    if "exit" in message or "quit" in message or "bye" in message:
        return "Goodbye! I hope to talk to you again soon."

    # === Default fallback response ===
    return "I'm not sure I understand. Can you rephrase that or ask something else?"
    
# ==== File Save/Load ====
def save_data():
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("history.json", "w") as f:
        json.dump(chat_history, f)

def load_data():
    global users, chat_history
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)
    if os.path.exists("history.json"):
        with open("history.json", "r") as f:
            chat_history = json.load(f)

# ==== Auth ====
def register():
    print(Colors.BLUE + "\n[REGISTER]" + Colors.RESET)
    username = input("New username: ")
    if username in users:
        print(Colors.RED + "Username already exists!" + Colors.RESET)
        return
    password = input("New password: ")
    role = input("Admin? (y/n): ")
    users[username] = {"password": password, "role": "admin" if role.lower() == 'y' else "user"}
    chat_history[username] = []
    save_data()
    print(Colors.GREEN + "Registration successful!" + Colors.RESET)

def login():
    print(Colors.BLUE + "\n[LOGIN]" + Colors.RESET)
    username = input("Username: ")
    password = input("Password: ")
    if username in users and users[username]["password"] == password:
        print(Colors.GREEN + f"Welcome, {username}!" + Colors.RESET)
        return username
    else:
        print(Colors.RED + "Login failed." + Colors.RESET)
        return None

# ==== Chatbot Session ====
def chat_session(username):
    print(Colors.YELLOW + "\n[CHATBOT MODE] Type 'exit' to end session.\n" + Colors.RESET)
    while True:
        message = input(f"{username} >> ")
        if message.lower() == "exit":
            break
        response = chatbot_response(message)
        print("AI >>", Colors.GREEN + response + Colors.RESET)
        chat_history[username].append({"user": message, "bot": response})
    save_data()

# ==== Admin Tools ====
def admin_menu():
    print(Colors.BLUE + "\n[ADMIN PANEL]" + Colors.RESET)
    for user, history in chat_history.items():
        print(f"\n--- Chat History: {user} ---")
        for chat in history:
            print(f"{user}: {chat['user']}")
            print(f"Bot: {chat['bot']}")

# ==== Main Menu ====
def main():
    load_data()
    while True:
        print(Colors.YELLOW + "\n=== AI CHATBOT CLI ===" + Colors.RESET)
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user = login()
            if user:
                if users[user]["role"] == "admin":
                    admin_menu()
                else:
                    chat_session(user)
        elif choice == "2":
            register()
        elif choice == "3":
            print(Colors.BLUE + "Goodbye!" + Colors.RESET)
            break
        else:
            print(Colors.RED + "Invalid choice!" + Colors.RESET)

if __name__ == "__main__":
    main()
