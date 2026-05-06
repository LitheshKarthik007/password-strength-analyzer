import tkinter as tk
import sqlite3
import string
import math

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT,
    score INTEGER,
    strength TEXT
)
""")

def has_upper(password):

    for ch in password:
        if ch.isupper():
            return True

    return False


def has_lower(password):

    for ch in password:
        if ch.islower():
            return True

    return False


def has_digit(password):

    for ch in password:
        if ch.isdigit():
            return True

    return False


def has_special(password):

    for ch in password:
        if ch in string.punctuation:
            return True

    return False


def has_sequence(password):

    for i in range(len(password) - 2):

        if ord(password[i]) + 1 == ord(password[i + 1]) and \
           ord(password[i]) + 2 == ord(password[i + 2]):

            return True

    return False


def calculate_score(length,
                    upper,
                    lower,
                    digit,
                    special,
                    sequence):

    score = 0

    if length >= 8:
        score += 20

    if upper:
        score += 20

    if lower:
        score += 20

    if digit:
        score += 20

    if special:
        score += 20

    if sequence:
        score -= 10

    return max(score, 0)


def password_strength(score):

    if score >= 90:
        return "Very Strong"

    elif score >= 70:
        return "Strong"

    elif score >= 50:
        return "Medium"

    else:
        return "Weak"


def entropy(length, charset):

    return round(length * math.log2(charset), 2)


def analyze_password():

    password = entry.get()

    upper = has_upper(password)
    lower = has_lower(password)
    digit = has_digit(password)
    special = has_special(password)
    sequence = has_sequence(password)

    score = calculate_score(
                len(password),
                upper,
                lower,
                digit,
                special,
                sequence
            )

    strength = password_strength(score)

    charset = 0

    if upper:
        charset += 26

    if lower:
        charset += 26

    if digit:
        charset += 10

    if special:
        charset += 32

    ent = entropy(len(password), charset)

    cursor.execute("""
    INSERT INTO passwords(password, score, strength)
    VALUES (?, ?, ?)
    """, (password, score, strength))

    conn.commit()

    result = f"""
Score : {score}/100

Strength : {strength}

Entropy : {ent} bits
"""

    if score >= 90:
        result += "\nEstimated Crack Time : Centuries"

    elif score >= 70:
        result += "\nEstimated Crack Time : Several Years"

    elif score >= 50:
        result += "\nEstimated Crack Time : Few Days"

    else:
        result += "\nEstimated Crack Time : Few Seconds"

    suggestion = "\n\nSuggestions:\n"

    if len(password) < 8:
        suggestion += "- Increase password length\n"

    if not upper:
        suggestion += "- Add uppercase letters\n"

    if not lower:
        suggestion += "- Add lowercase letters\n"

    if not digit:
        suggestion += "- Include numbers\n"

    if not special:
        suggestion += "- Include special characters\n"

    if sequence:
        suggestion += "- Avoid sequential patterns\n"

    output.config(text=result + suggestion)


root = tk.Tk()

root.title("Password Strength Analyzer")
root.geometry("500x500")
root.configure(bg="#0f172a")

title = tk.Label(
            root,
            text="Password Strength Analyzer",
            font=("Arial", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )

title.pack(pady=20)

entry = tk.Entry(
            root,
            width=30,
            font=("Arial", 16),
            show="*"
        )

entry.pack(pady=20)

button = tk.Button(
            root,
            text="Analyze Password",
            font=("Arial", 14),
            bg="#22c55e",
            fg="black",
            command=analyze_password
        )

button.pack(pady=10)

output = tk.Label(
            root,
            text="",
            justify="left",
            font=("Arial", 12),
            bg="#0f172a",
            fg="white"
        )

output.pack(pady=20)

root.mainloop()

conn.close()
