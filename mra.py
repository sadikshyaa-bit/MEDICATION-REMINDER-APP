import json
import time
import winsound
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ══════════════════════════════════════════
#   COLORS  (plain ANSI codes, no library)
# ══════════════════════════════════════════

# Background colors
LIGHT_BLUE = "\033[48;2;173;216;230m"   # light blue background
SKY_BLUE   = "\033[48;2;135;206;250m"   # sky blue background (for headers)

# Text colors
NAVY       = "\033[38;2;0;31;84m"       # dark navy text
WHITE      = "\033[38;2;255;255;255m"   # white text
BOLD       = "\033[1m"                  # bold text
GREEN      = "\033[38;2;0;150;80m"      # green  (success)
RED        = "\033[38;2;200;30;30m"     # red    (error)
YELLOW     = "\033[38;2;180;120;0m"     # yellow (warning)

# Reset — always put this at the end of a colored print
RESET      = "\033[0m"


# ══════════════════════════════════════════
#   HELPER FUNCTIONS
# ══════════════════════════════════════════

def spacer():
    print()

def print_header(text):
    print(SKY_BLUE + WHITE + BOLD + "  " + text + "  " + RESET)

def print_row(text):
    print(LIGHT_BLUE + NAVY + "  " + text + "  " + RESET)

def print_ok(msg):
    print(GREEN + "  ✔  " + msg + RESET)

def print_err(msg):
    print(RED + "  ✖  " + msg + RESET)

def print_warn(msg):
    print(YELLOW + "  ⚠  " + msg + RESET)

def ask(label):
    answer = input(LIGHT_BLUE + NAVY + "  " + label + ": " + RESET + "  ")
    return answer.strip()


# ══════════════════════════════════════════
#   DATA  (save/load users.json)
# ══════════════════════════════════════════

def load_data():
    try:
        file = open("users.json", "r")
        data = json.load(file)
        file.close()
        return data
    except FileNotFoundError:
        return {"users": {}}

def save_data(data):
    file = open("users.json", "w")
    json.dump(data, file, indent=4)
    file.close()

data = load_data()


# ══════════════════════════════════════════
#   REGISTER
# ══════════════════════════════════════════


def register():

    print("\n" * 2)
    
    title = " REGISTRATION "
    print("╔" + "═"*40 + "╗")
    print("║" + title.center(40) + "║")
    print("╚" + "═"*40 + "╝")

    print()

    username = input("👤 Create Username : ")
    password = input("🔒 Create Password : ")

    if len(password) < 8:
        print("\n❌ Password must be at least 8 characters!")
        return

    if not any(char.isdigit() for char in password):
        print("\n❌ Password must contain at least one number!")
        return

    if not any(char.isupper() for char in password):
        print("\n❌ Password must contain at least one capital letter!")
        return

    if username == "" or password == "":
        print("\n❌ Fields cannot be empty!")
        return

    if username in data["users"]:
        print("\n❌ Username already exists!")
        return 

    data["users"][username] = {
    "password": hash_password(password),
    "medications": []
}

    save_data(data)

    print("\n✅ Registration Successful!")
    input("\nPress Enter to continue...")

#══════════════════════════════════════════
#   LOGIN
# ══════════════════════════════════════════

def login():
    spacer()
    title = "  LOGIN 🔐 "

    print("╔" + "═"*40 + "╗")
    print("║" + title.center(40) + "║")
    print("╚" + "═"*40 + "╝")

    username = ask("Username 👤 ")
    print()
    password = ask("Password 🔒 ")

    if username in data["users"]:

        if data["users"][username]["password"] == hash_password(password):
            print_ok("✅ Login successful ✅")
            home(username)
        else:
            print_err("❌ Incorrect password ❌")

    else:
        print_err("❌ Username not found ❌")
        
# ══════════════════════════════════════════
#   ADD MEDICATION
# ══════════════════════════════════════════

def add_medication(username):
    print("\n")
    print("╔" + "═"*40 + "╗")
    print("║" + " ADD MEDICATION 💊".center(40) + "║")
    print("╚" + "═"*40 + "╝\n")

    med_name = input("💊 Enter Medicine Name    : ").strip()
    if not med_name:
        print("❌ Medicine name cannot be empty!")
        return

    # Keep asking until valid time and date are entered
    while True:
        med_time = input("⏰ Time (HH:MM)      : ").strip()
        med_date = input("📅 Date (YYYY/MM/DD) : ").strip()

        try:
            med_datetime = datetime.strptime(f"{med_date} {med_time}", "%Y/%m/%d %H:%M")
        except ValueError:
            print("❌ Wrong format! Use HH:MM for time and YYYY/MM/DD for date. Try again!\n")
            continue  # ← go back to top of loop

        current_datetime = datetime.now()
        if med_datetime < current_datetime:
            print("❌ Date and time cannot be in the past. Try again!\n")
            continue  # ← go back to top of loop

        break  # ← everything is valid, exit loop

    # Save
    data["users"][username]["medications"].append({
        "name": med_name,
        "time": med_time,
        "date": med_date
    })
    save_data(data)
    print("✅ Medication Added Successfully!")