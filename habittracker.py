import datetime
import json
import os
import questionary

FILENAME = "habits.json"

# Minimalist ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
DIM = "\033[2m"


def clear_screen():
    """Clears the terminal screen for a smooth TUI view."""
    os.system("cls" if os.name == "nt" else "clear")


def load_habits():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return {}


def save_habits():
    with open(FILENAME, "w") as f:
        json.dump(my_habits, f, indent=4)


def display_grid():
    """Renders a dynamic 7-day weekly table fitting mobile screens."""
    today = datetime.date.today()
    
    # Get current week (Monday to Sunday)
    start_of_week = today - datetime.timedelta(days=today.weekday())
    week_days = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
    num_days = 7

    week_range_str = f"{week_days[0].strftime('%b %d')} - {week_days[-1].strftime('%b %d, %Y')}"

    # Header Row (Day numbers)
    day_headers = "".join(f"{str(d.day).center(3)}│" for d in week_days)
    header_line = f"│ {BOLD}{CYAN}{'Habits':<12}{RESET} │{day_headers}"

    # Dynamic Borders matching 7 columns
    top_border = "┌" + "─" * 14 + "┬" + ("───┬" * (num_days - 1)) + "───┐"
    divider = "├" + "─" * 14 + "┼" + ("───┼" * (num_days - 1)) + "───┤"
    bottom_border = "└" + "─" * 14 + "┴" + ("───┴" * (num_days - 1)) + "───┘"

    print(f"\n {BOLD}--- HABIT TRACKER ({week_range_str}) ---{RESET}\n")
    print(top_border)
    print(header_line)
    print(divider)

    # Habit Rows
    if not my_habits:
        empty_row = (
            f"│ {DIM}{'No habits yet':<12}{RESET} │"
            + "".join(f" {DIM}·{RESET} │" for _ in range(num_days))
        )
        print(empty_row)
    else:
        for habit_name, days_dict in my_habits.items():
            formatted_days = []
            for d in week_days:
                date_key = d.isoformat()  # Format: 'YYYY-MM-DD'
                val = days_dict.get(date_key, " ")
                if val in ["✔", "x", "X"]:
                    formatted_days.append(f" {GREEN}✔{RESET} ")
                else:
                    formatted_days.append(f" {DIM}·{RESET} ")

            row_str = "│".join(formatted_days)
            print(f"│ {BOLD}{habit_name:<12}{RESET} │{row_str}│")

    print(bottom_border)
    print()


# --- APP MAIN LOOP ---
my_habits = load_habits()

while True:
    clear_screen()
    display_grid()

    choice = questionary.select(
        "Action:",
        choices=[
            "1) Add Habit",
            "2) Mark Habit Done",
            "3) UnMark Habit Done",
            "0) Quit",
        ],
        pointer="❯",
    ).ask()

    if choice is None or choice.startswith("0"):
        save_habits()
        print(f"\n{GREEN}Habits saved. Goodbye!{RESET}\n")
        break

    elif choice.startswith("1"):
        new_habit = questionary.text("Enter new habit name:").ask()
        if new_habit:
            new_habit = new_habit.strip()
            if new_habit not in my_habits:
                my_habits[new_habit] = {}
                save_habits()

    elif choice.startswith("2"):
        if not my_habits:
            continue
        chosen_habit = questionary.select(
            "Choose habit to mark done:", choices=list(my_habits.keys()), pointer="❯"
        ).ask()
        if chosen_habit:
            today_key = datetime.date.today().isoformat()
            my_habits[chosen_habit][today_key] = "✔"
            save_habits()

    elif choice.startswith("3"):
        if not my_habits:
            continue
        chosen_habit = questionary.select(
            "Choose habit to unmark:", choices=list(my_habits.keys()), pointer="❯"
        ).ask()
        if chosen_habit:
            today_key = datetime.date.today().isoformat()
            my_habits[chosen_habit][today_key] = " "
            save_habits()