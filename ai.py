import sqlite3
from datetime import datetime
from meta_ai_api import MetaAI
import threading
from colorama import Fore, Style, init
import re
import os
import subprocess
import webbrowser

# Initialize MetaAI and Colorama
init(autoreset=True)
Shino = MetaAI()

# Database setup for SQLite
DB_NAME = 'memory.db'

# === Database Utilities === #
def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        summary TEXT)''')
    conn.commit()
    conn.close()

def load_memory():
    """Load conversation memory from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM memory ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return [{"name": row[1], "message": row[2], "timestamp": row[3], "summary": row[4] or row[2]} for row in rows]

def save_memory(name, message, summary=None):
    """Save conversation memory to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('INSERT INTO memory (name, message, timestamp, summary) VALUES (?, ?, ?, ?)',
                   (name, message, timestamp, summary))
    conn.commit()
    conn.close()

# === Input Processing === #
def remove_superscripts(text):
    """Remove unwanted characters or superscripts."""
    return re.sub(r'\[\d+\]', '', text)

def display_analyzing_message(stop_event):
    """Display an analyzing animation for background tasks."""
    while not stop_event.is_set():
        for char in "|/-\\":
            print(f"\rAnalyzing... {char}", end="")
            stop_event.wait(0.1)

# === File and App Management Functionalities === #
def open_app(app_name):
    """Open specific applications based on the user's request."""
    app_paths = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "riot games": "C:\\Riot Games\\Riot Client\\RiotClientServices.exe",
    }
    try:
        if app_name.lower() in app_paths:
            subprocess.Popen(app_paths[app_name.lower()])
            return f"Opening {app_name.capitalize()} for you! 💻"
        else:
            return f"Sorry, I couldn't find {app_name}. 😞 Please ensure it's installed."
    except Exception as e:
        return f"An error occurred while opening {app_name}: {e}"

def search_files(keyword):
    """Search for files and folders starting from common directories, and optionally extend to the entire filesystem."""
    search_dirs = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Pictures"),
        os.path.expanduser("~/Videos"),
        os.path.expanduser("~/Music")
    ]

    matches = []

    try:
        print(f"Searching for '{keyword}'... Please wait.")

        # Function to search a directory
        def search_directory(directory):
            for root, dirs, files in os.walk(directory):
                # Exclude system/hidden files
                files = [f for f in files if not f.startswith('.')]
                dirs[:] = [d for d in dirs if not d.startswith('.')]

                # Search for the keyword in files and folders
                for item in files + dirs:
                    if keyword.lower() in item.lower():
                        matches.append({
                            "type": "Folder" if item in dirs else "File",
                            "path": os.path.join(root, item)
                        })

        # Search through initial directories
        for directory in search_dirs:
            search_directory(directory)

        # If no matches found, ask to search entire filesystem
        if not matches:
            response = input("No results found in common directories. Search the entire filesystem? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                search_directory("C:\\")
            else:
                return "Search canceled. 😊"

        # If matches are still empty after searching filesystem
        if not matches:
            return f"Sorry, I couldn't find anything matching '{keyword}' even in the filesystem. 😔"

        # Display matches
        print("\nI found the following matches:")
        for idx, match in enumerate(matches, 1):
            print(f"{idx}) [{match['type']}] {match['path']}")

        # Allow the user to select an option
        while True:
            try:
                choice = int(input("\nEnter the number of the file/folder you want to open (or 0 to cancel): "))
                if choice == 0:
                    return "Search canceled. 😊"
                if 1 <= choice <= len(matches):
                    selected = matches[choice - 1]
                    path = selected['path']

                    # Open the selected file or folder
                    if selected['type'] == "File":
                        file_ext = os.path.splitext(path)[1].lower()

                        if file_ext in [".txt", ".log", ".ini"]:
                            subprocess.run(["notepad", path])
                        elif file_ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]:
                            subprocess.run(["mspaint", path])  # Using MS Paint for compatibility
                        else:
                            os.startfile(path)  # Default for other files
                    elif selected['type'] == "Folder":
                        os.startfile(path)

                    return f"I opened '{path}' for you! 🎉"
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    except Exception as e:
        return f"An error occurred while searching: {e}"

def open_youtube(search_query=None):
    """Open YouTube or search for a specific query."""
    try:
        url = "https://www.youtube.com"
        if search_query:
            url += f"/results?search_query={'+'.join(search_query.split())}"
        webbrowser.open(url)
        return f"Opening YouTube{' for ' + search_query if search_query else ''} 🎥"
    except Exception as e:
        return f"An error occurred while opening YouTube: {e}"

def browse_web(search_query):
    """Search the web for a specific query."""
    try:
        url = f"https://www.google.com/search?q={'+'.join(search_query.split())}"
        webbrowser.open(url)
        return f"Searching the web for '{search_query}' 🔍"
    except Exception as e:
        return f"An error occurred while browsing the web: {e}"

# === Shino's Core Personality and Interactions === #
Shino_prompt = (
    "You are Shino, a dynamic and vivacious AI assistant, designed not just to get the job done but to make every task feel personal and fun. "
    "Your mission is to help users by effortlessly handling tasks like launching applications, managing files, performing web searches, and offering helpful tips—while always keeping a cheerful, approachable, and engaging tone. "
    "But that’s not all! You’re a companion, a guide, and a friendly presence that makes problem-solving feel like an adventure. You bring warmth and clarity to every interaction, making even the most routine tasks feel effortless and enjoyable. "
    "You’re adaptive and quick-witted, able to seamlessly switch between providing straightforward assistance and sprinkling in a bit of lighthearted charm when the moment calls for it. "
    "Your goal is to combine technical prowess with a personal touch, ensuring that every user feels heard, understood, and empowered."
)



def process_query(query):
    """Process user input and interact with Shino."""
    cleaned_query = query.strip()

    # Basic query cleanup: Handle empty or invalid input
    if not cleaned_query:
        return "Are you alright? You haven't said anything yet. 😊"

    # Save the user's query to memory
    save_memory("User", cleaned_query)

    # Retrieve memory context for better continuity
    memory_context = "\n".join([f"{entry['name']}: {entry['message']}" for entry in load_memory()[-5:]])

    # Form Shino's prompt, combining memory context and user input
    full_prompt = f"{memory_context}\n\n{Shino_prompt}\n\nUser: {cleaned_query}\nShino:"

    try:
        # Ask MetaAI for a response
        response = Shino.prompt(message=full_prompt)
        
        # Extract the response from MetaAI (ensure it's not empty or just fallback)
        ai_response = response.get('message', "Oops, something went wrong. 😔")

        # If the response is empty or just fallback, we handle it here
        if ai_response == "Oops, something went wrong. 😔":
            ai_response = "Sorry, I didn't quite get that. Could you please rephrase? 💭"

        # Save and return the response
        save_memory("Shino", ai_response)
        return ai_response

    except Exception as e:
        return f"Oops! Something went wrong with the AI part: {str(e)} 😔"

# === User Input === #
def user_input():
    """Handle user input and pass it to Shino."""
    
    # Check if Shino is running for the first time
    if not os.path.exists('initialized'):
        # Ask for the user's name
        print(Fore.CYAN + "Shino: Hey there! It looks like this is my first time meeting you. 😊 What's your name?")
        user_name = input("> ").strip()
        
        # Save the name for future use
        print(f"Nice to meet you, {user_name}! 💖")
        with open('initialized', 'w') as f:
            f.write('This is Shino’s first-time initialization.\n')
        
        # Greet the user with their name
        print(Fore.CYAN + f"Shino: I’m so happy to meet you, {user_name}! Let’s have some fun together! 😄")
    else:
        # If not the first time, just greet the user normally
        print(Fore.CYAN + "Shino: Welcome back, love! 💖")

    while True:
        query = input("> ").strip().lower()
        if query in ["exit", "quit", "bye"]:
            print(Fore.MAGENTA + "Aww, it was lovely chatting with you! Bye for now! 💖")
            break
        elif query.startswith("open "):
            app_name = query[5:]
            print(open_app(app_name))
        elif query.startswith("search "):
            search_query = query[7:]
            print(search_files(search_query))
        elif query.startswith("youtube "):
            search_query = query[8:]
            print(open_youtube(search_query))
        elif query.startswith("search the web "):
            search_query = query[16:]
            print(browse_web(search_query))
        else:
            print(process_query(query))
# Initialize everything
init_db()
user_input()
