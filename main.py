from tkinter import *
from random import choice, randint, shuffle
from tkinter import messagebox
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_gen():
    password = password_entry.get()
    pw_l = [choice(letters) for _ in range(randint(6, 10))]
    pw_s = [choice(symbols) for _ in range(randint(2, 4))]
    pw_z = [choice(numbers) for _ in range(randint(2, 4))]
    pw_list = pw_l + pw_z + pw_s
    shuffle(pw_list)
    nw_pw = "".join(pw_list)
    if len(password) == 0:
        password_entry.insert(0, nw_pw)
    else:
        messagebox.showinfo(title="Oops", message="Looks like you already have a password.")
    pyperclip.copy(f'{password}')


# ---------------------------- SAVE PASSWORD ------------------------------- #
# Write data to the data file
def data_write():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
    }}
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Looks like you left a field empty.")

    else:
        try:
            with open("data.json", "r") as manager:
                # Reads the old data
                data = json.load(manager)
        except FileNotFoundError:
            with open("data.json", "w") as manager:
                json.dump(new_data, manager, indent=4)
        else:
            # updates with the new data
            data.update(new_data)
            with open("data.json", "w") as manager:
                # saves the new data
                json.dump(data, manager, indent=4)
        finally:
            # delete the website and password info
            website_entry.delete(0, END)
            password_entry.delete(0, END)
#           email_entry.delete(0, END) if I feel like adding it


# When the add btn is clicked it will act upon the above functions
def add_button():
    data_write()


def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as manager:
            data = json.load(manager)
    except FileNotFoundError:
        messagebox.showinfo(title="Result", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Result", message=f"Found it!\nEmail: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Result", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("My Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# website input
website_label = Label(text="Website:    ")
website_label.grid(column=0, row=1)
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=1, column=1)
search_btn = Button(text="Search", width=14, command=find_password)
search_btn.grid(column=2, row=1)

# email/username input
email_label = Label(text="Email/Username:    ")
email_label.grid(column=0, row=2)
email_entry = Entry(width=36)
email_entry.insert(0, "indigo@email.com")
email_entry.grid(row=2, column=1, columnspan=2)

# password input
password_label = Label(text="Password:    ")
password_label.grid(column=0, row=3)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)
pyperclip.copy(f"{password_entry.get}")
password_btn = Button(text="Generate Password", command=password_gen, width=14)
password_btn.grid(column=2, row=3)

# add button
add_btn = Button(text="Add", width=36, command=add_button)
add_btn.grid(column=1, row=4, columnspan=2)

window.mainloop()

# with open("data.json", "r") as manager:
#     # to write ("data.json", "w")
#     # json.dump(new_data, manager, indent=4)
#     # to read and load as a dictionary
#     # data = json.load(manager)
#     # print(data)
#     # update data, reading old data, updating data with new data and saving the new data
#     data = json.load(manager)
#     data.update(new_data)
# with open("data.json", "w") as manager:
#     # saves the new data
#     json.dump(data, manager, indent=4)
#     # manager.writelines(f"{website} | {email} | {password}\n")
