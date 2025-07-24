import tkinter as tk
import random
from datetime import datetime


# Weekday names
weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

month_hints = [
    "January 3",
    "February 28",
    "March 14 (pi day)",
    "April 4 (4/4, 6/6, 8/8, 10/10, 12/12)",
    "May 9 (9-5 at the 7-Eleven)",
    "June 6 (4/4, 6/6, 8/8, 10/10, 12/12)",
    "July 11 (9-5 at the 7-Eleven)",
    "August 8 (4/4, 6/6, 8/8, 10/10, 12/12)",
    "September 5 (9-5 at the 7-Eleven)",
    "October 10 (4/4, 6/6, 8/8, 10/10, 12/12)",
    "November 7 (9-5 at the 7-Eleven)",
    "December 12 (4/4, 6/6, 8/8, 10/10, 12/12)",
]
month_doomsdays = [3, 28, 14, 4, 9, 6, 11, 8, 5, 10, 7, 12]

leap_year_month_hints = [
    "January 4 (Leap Year)",
    "February 29 (Leap Year)",
]

def leap_year(year):     
    if 0 == year % 400:
        return True
    if 0 == year % 100:
        return False
    if year % 4:
        return False
    return True

hint_step = 0
hint_text = " "*120
hint_century_anchor_day = 0
hint_two_digit_year = 0
hint_leap_year = False
hint_year_doomsday_a = 0
hint_year_doomsday_b = 0
hint_year_doomsday_c = 0
hint_year_doomsday = 0
hint_month_doomsday = 0

def hint():
    global hint_step, hint_text, hint_century_anchor_day, hint_two_digit_year
    global hint_year_doomsday_a, hint_year_doomsday_b, hint_year_doomsday_c
    global hint_year_doomsday, hint_month_doomsday

    if hint_step == 0:
        hint_step = 1
        century = random_date.year // 100
        if century == 18:
            hint_century_anchor_day = 5
        elif century == 19:
            hint_century_anchor_day = 3
        else:
            hint_century_anchor_day = 2
        hint_text = hint_text + "\n1. Memorize the century anchor day = "
        hint_text = hint_text + f"{hint_century_anchor_day}"
        hint_text = hint_text + "\n    weekdays start at 0 for Sunday to 6 for Saturday"
    elif hint_step == 1:
        hint_two_digit_year = (random_date.year % 100)
        hint_year_doomsday_a = hint_two_digit_year // 12
        hint_text = hint_text + "\n2. Integer divide last 2 digits of the year by 12. "
        hint_text = hint_text + f"Call it A:\n    A = {hint_two_digit_year}/12 = "
        hint_text = hint_text + f"{hint_year_doomsday_a}"
        hint_step = 2
    elif hint_step == 2:
        hint_year_doomsday_b = hint_two_digit_year % 12
        hint_text = hint_text + "\n3. Remainder of above. Call it B:\n    B = "
        hint_text = hint_text + f"{hint_two_digit_year}%12 = {hint_year_doomsday_b}"
        hint_step = 3
        label.config(text=hint_text)
    elif hint_step == 3:
        hint_year_doomsday_c = hint_year_doomsday_b // 4
        hint_text = hint_text + "\n4. Integer divide remainder B by 4. "
        hint_text = hint_text + f"Call it C:\n    C = {hint_year_doomsday_b}/4 = "
        hint_text = hint_text + f"{hint_year_doomsday_c}"
        hint_step = 4
    elif hint_step == 4:
        hint_year_doomsday = (
            hint_century_anchor_day + hint_year_doomsday_a + hint_year_doomsday_b
            + hint_year_doomsday_c
        )
        hint_text = hint_text + "\n5. Add all of the above, modulo 7: \n    "
        hint_text = hint_text + f"{hint_century_anchor_day}+{hint_year_doomsday_a}+"
        hint_text = hint_text + f"{hint_year_doomsday_b}+{hint_year_doomsday_c} = "
        hint_text = hint_text + f"{hint_year_doomsday}"
        if hint_year_doomsday > 6:
            hint_text = hint_text + f"\n    {hint_year_doomsday}%7="
            hint_year_doomsday %= 7
        hint_text = hint_text + f"{hint_year_doomsday} {weekdays[hint_year_doomsday]}."
        hint_text = hint_text + "\n    This is the year's doomsday"
        hint_step = 5
    elif hint_step == 5:
        hint_step = 6
        if leap_year(random_date.year):
            month_doomsdays[0] = 4
            month_doomsdays[1] = 29
            month_hints[0] = leap_year_month_hints[0]
            month_hints[1] = leap_year_month_hints[1]
        else:
            month_hints[0] = "January 3"
            month_hints[1] = "February 28"
            month_doomsdays[0] = 3
            month_doomsdays[1] = 28

        hint_text = hint_text + f"\n6. The doomsday for this month is {month_hints[random_date.month-1]}"
        hint_month_doomsday = month_doomsdays[random_date.month-1]
    elif hint_step == 6:
        hint_step = 7
        day_str = "day" if abs(hint_month_doomsday-random_date.day) == 1 else "days"
        direction_str = "backward" if hint_month_doomsday-random_date.day > 0 else "forward"
        if hint_month_doomsday == random_date.day:
            hint_text = hint_text + "\n7. That's the day we're checking. The answer is "
            answer = hint_year_doomsday
        else:
            hint_text = hint_text + f"\n7. Count {direction_str} "
            hint_text = hint_text + f"{abs(hint_month_doomsday-random_date.day)} {day_str}"
            hint_text = hint_text + f"\n    from doomsday {hint_year_doomsday}, modulo 7."
            answer = hint_year_doomsday + (random_date.day - hint_month_doomsday)
            answer %= 7
        hint_text = hint_text + f"\n    {answer} or {weekdays[answer]}"


    label.config(text=hint_text)

def button_clicked(day):
    weekday = (random_date.weekday() + 1) % 7
    if day == weekday:
        label1.config(text=f"Correct!: {weekdays[day]}")
    else:
        label1.config(text=f"Incorrect")

def generate_random_date():
    dpm = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # Generate a (mostly) random year, month, and day
    year = random.randint(1801, 2050)

    # Special case: if a leap year, choose Jan/Feb half the time
    if leap_year(year) and random.choice([True, False]):
        days = 366
        dpm[1] = 29
        day = random.randint(1, 60)
    else:
        days = 365
        day = random.randint(1, days)
    month = 1
    while day > dpm[month-1]:
        day -= dpm[month-1]
        month += 1
    random_date = datetime(year, month, day)
    return random_date

def restart():
    global random_date, hint_step, hint_text, label
    random_date = generate_random_date()
    date_label.config(text=f" {random_date.strftime('%B ')}{random_date.day}, {random_date.strftime('%Y')}")
    hint_step = 0
    label1.config(text="Figure the weekday for the date")
    hint_text = " "*120
    label.config(text=hint_text)


# Create the main window
root = tk.Tk()
root.title("Doomsday")

# Generate a random date and display it
random_date = generate_random_date()
random_date_weekday = (random_date.weekday() + 1) % 7
date_label = tk.Label(root, text=f" {random_date.strftime('%B ')}{random_date.day}, {random_date.strftime('%Y')}")
date_label.pack(pady=10)

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

# Create buttons for each day of the week
for day in range(7):
    btn = tk.Button(
        button_frame,
        text=weekdays[day],
        width=10,
        command=lambda d=day: button_clicked(d),
    )
    btn.pack(side=tk.LEFT, padx=2)

# Add the Hint button
hint_button = tk.Button(root, text="Hint", command=lambda: hint())
hint_button.pack(pady=10)

label1 = tk.Label(root, text="Figure the weekday for the date")
label1.pack(pady=10)

# Label to show hints
label = tk.Label(root, text=hint_text, justify=tk.LEFT)
label.pack(pady=10)

# Add Restart button
restart_button = tk.Button(root, text="Restart", command=lambda: restart())
restart_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
