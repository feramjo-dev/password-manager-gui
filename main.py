from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
           'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# Constants
WHITE = "#fff"
PASSWORD_FILE = "password_data.json"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    generated_password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, string=generated_password)
    pyperclip.copy(text=generated_password)


# ---------------------------- JSON FILE UTILITIES ------------------------------- #
def load_password_data():
    try:
        with open(PASSWORD_FILE, mode="r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_password_data(data):
    with open(PASSWORD_FILE, mode="w") as file:
        json.dump(data, file, indent=4)


# ---------------------------- DIALOG HELPER ------------------------------- #
def confirm_action(website, email, password, is_update=False):
    if is_update:
        msg = f"Details for '{website}' already exist.\n\nUpdate with:\nEmail: {email}\nPassword: {password}"
        return messagebox.askokcancel(title="Update Confirmation", message=msg)
    else:
        msg = f"Please confirm the details:\n\nWebsite: {website}\nEmail: {email}\nPassword: {password}"
        return messagebox.askokcancel(title="Confirm Details", message=msg)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    new_website = website_entry.get().strip()
    new_email = email_entry.get().strip()
    new_password = password_entry.get().strip()

    if not new_website or not new_email or not new_password:
        messagebox.showerror(title="Oops", message="Please fill in all the details!")
        return

    new_data = {
        new_website.lower(): {
            "email": new_email,
            "password": new_password
        }
    }

    password_data = load_password_data()
    saved_websites = [website.lower() for website in password_data]
    is_update = new_website.lower() in saved_websites

    if not confirm_action(new_website, new_email, new_password, is_update=is_update):
        return

    password_data.update(new_data)
    save_password_data(password_data)

    website_entry.delete(0, END)
    email_entry.delete(0, END)
    email_entry.insert(0, string="example@example.com")
    password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website_name = website_entry.get().strip().lower()

    if not website_name:
        messagebox.showerror(title="Oops", message="Please enter a website to search.")
        return

    password_data = load_password_data()
    saved_websites = [website.lower() for website in password_data]

    if len(saved_websites) == 0:
        messagebox.showerror(message="No passwords saved yet")
    elif website_name not in saved_websites:
        messagebox.showinfo(title="Oops", message=f'"{website_name.upper()}" password data not found')
        return
    else:
        for (key, value) in password_data.items():
            if key.lower() == website_name:
                website_email = value["email"]
                website_password = value["password"]
                messagebox.showinfo(title=website_name, message=f"Email: {website_email}\nPassword: "
                                                                f"{website_password}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WHITE)

# Setup canvas
canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# ==== Setup forms ====

# Website input
website_label = Label(text="Website:", bg=WHITE)
website_label.grid(column=0, row=1)

website_entry = Entry(width=32)
website_entry.focus()
website_entry.grid(column=1, row=1)

# Search Button
search_button = Button(text="Search", bg=WHITE, width=14, command=search_password)
search_button.grid(column=2, row=1)

# Email input
email_label = Label(text="Email/Username:", bg=WHITE)
email_label.grid(column=0, row=2)

email_entry = Entry(width=50)
email_entry.insert(0, string="example@example.com")
email_entry.grid(column=1, row=2, columnspan=2)

# Password input
password_label = Label(text="Password:", bg=WHITE)
password_label.grid(column=0, row=3)

password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password", bg=WHITE, command=generate_password)
generate_password_button.grid(column=2, row=3)

# Add password button
add_password_btn = Button(text="Add", bg=WHITE, width=43, command=save_password)
add_password_btn.grid(column=1, row=4, columnspan=2)


window.mainloop()