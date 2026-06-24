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

# ══════════════════════════════════════════
#   VIEW MEDICATIONS
# ══════════════════════════════════════════

def view_medications(username):

    meds = data["users"][username]["medications"]

    if len(meds) == 0:
        print("❌ No medications found!")
        return
    print("\n════════ YOUR MEDICATIONS ════════\n")

    for i, med in enumerate(meds, start=1):

        print(
            f"{i}. 💊 {med['name']}\n"
            f"   ⏰ Time : {med['time']}\n"
            f"   📅 Date : {med['date']}\n"
        )

# ══════════════════════════════════════════
#   REMOVE MEDICATION
# ══════════════════════════════════════════

def clear_medications(username):

    meds = data["users"][username]["medications"]

    if len(meds) == 0:
        print("❌ No medications found!")
        return

    print("\nYour Medications:")

    for i in range(len(meds)):
        print(i + 1, "-", meds[i]["name"])

    try:
        choice = int(input("\n👉 Enter medication number to remove: "))
    except ValueError:
        print("❌ Enter a valid number!")
        return
    if 1 <= choice <= len(meds):

        removed = meds[choice - 1]["name"]

        meds.pop(choice - 1)

        save_data(data)

        print("✅", removed, "removed successfully!")

    else:
        print("❌ Invalid choice!")


# ══════════════════════════════════════════
#   REMINDERS
# ══════════════════════════════════════════

def start_reminders(username):

    spacer()
    title = "🔔 REMINDER 🔔 "

    print("╔" + "═"*40 + "╗")
    print("║" + title.center(40) + "║")
    print("╚" + "═"*40 + "╝")

    print("\nChecking every 5 seconds. Press Ctrl+C to stop.")

    reminded = set()

    try:
        while True:

            current_time = datetime.now().strftime("%H:%M")
            current_date = datetime.now().strftime("%Y/%m/%d")

            meds = data["users"][username]["medications"]

            for med in meds:

                reminder_id = (
                    med["name"],
                    med["date"],
                    med["time"]
                )

                if (
                    med["time"] == current_time
                    and med["date"] == current_date
                    and reminder_id not in reminded
                ):

                    print()
                    print(SKY_BLUE + WHITE + BOLD +
                          f" 🔔 TAKE {med['name']} NOW! 🔔 "
                          + RESET)

                    winsound.Beep(1000, 2000)

                    reminded.add(reminder_id)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🔕 Reminders stopped.")
    

