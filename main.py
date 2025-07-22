from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
           'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# Constants
WHITE = "#fff"


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


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    new_website = website_entry.get()
    new_email = email_entry.get()
    new_password = password_entry.get()

    if not new_website or not new_email or not new_password:
        messagebox.showerror(title="Oops", message="Please fill in all the details!")
        return

    is_ok = messagebox.askokcancel(title=new_website, message=f"Please confirm your details before you proceed to "
                                                              f"save!\n\nEmail: {new_email}\nPassword: {new_password}")

    if is_ok:
        with open ("password.txt", mode="a") as password_file:
            password_file.write(f"{new_website} | {new_email} | {new_password}\n")

        website_entry.delete(0, END)
        email_entry.delete(0, END)
        email_entry.insert(0, string="ojoemmanuel935@gmail.com")
        password_entry.delete(0, END)


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

website_entry = Entry(width=50)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)
email_label = Label(text="Email/Username:", bg=WHITE)
email_label.grid(column=0, row=2)

email_entry = Entry(width=50)
email_entry.insert(0, string="ojoemmanuel935@gmail.com")
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