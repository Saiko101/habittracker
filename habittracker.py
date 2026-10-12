import calendar
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
    """Renders a dynamic box-drawing table based on the current month and year."""
    today = datetime.date.today()
    year = today.year
    month = today.month
    
    # Get the exact number of days in the current month (handles 28, 30, 31 automatically!)
    num_days = calendar.monthrange(year, month)[1]
    month_name = calendar.month_name[month].upper()

    # Header Row
    day_headers = "".join(f"{str(day).center(3)}│" for day in range(1, num_days + 1))
    header_line = f"│ {BOLD}{CYAN}{'Habits':<12}{RESET} │{day_headers}"

    # Dynamic Borders matching the number of days
    top_border = "┌" + "─" * 14 + "┬" + ("───┬" * (num_days - 1)) + "───┐"
    divider = "├" + "─" * 14 + "┼" + ("───┼" * (num_days - 1)) + "───┤"
    bottom_border = "└" + "─" * 14 + "┴" + ("───┴" * (num_days - 1)) + "───┘"

    print(f"\n {BOLD}--- JOURNAL HABIT TRACKER ({month_name} {year}) ---{RESET}\n")
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
            for d in range(1, num_days + 1):
                val = days_dict.get(str(d), " ")
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
                # Initialize slots for all days of the current month
                today = datetime.date.today()
                num_days = calendar.monthrange(today.year, today.month)[1]
                my_habits[new_habit] = {
                    str(day): " " for day in range(1, num_days + 1)
                }
                save_habits()

    elif choice.startswith("2"):
        if not my_habits:
            continue
        chosen_habit = questionary.select(
            "Choose habit to mark done:", choices=list(my_habits.keys()), pointer="❯"
        ).ask()
        if chosen_habit:
            today_day = str(datetime.date.today().day)
            # Ensure day exists in dict just in case of month shifts
            if today_day in my_habits[chosen_habit]:
                my_habits[chosen_habit][today_day] = "✔"
                save_habits()

    elif choice.startswith("3"):
        if not my_habits:
            continue
        chosen_habit = questionary.select(
            "Choose habit to unmark:", choices=list(my_habits.keys()), pointer="❯"
        ).ask()
        if chosen_habit:
            today_day = str(datetime.date.today().day)
            if today_day in my_habits[chosen_habit]:
                my_habits[chosen_habit][today_day] = " "
                save_habits()