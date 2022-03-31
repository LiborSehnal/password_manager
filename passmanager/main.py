from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# GENEROVÁNÍ HESLA #

def generate_password():
    # arrays pro random choice
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    # výběr náhodných znaků pro tři listy
    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    # vše se dá dohromady a zamíchá
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    # vygenerované heslo se rovnou vloží do ctrlC
    pyperclip.copy(password)


# VALIDACE A ULOŽENÍ FORMU #

def uloz():
    # uložení vstupů do proměnných
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # showinfo při částečném/kompletním nevyplnění
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="chyba", message="Nevyplnil jsi všechny položky.")
    # načtení, update a zápis dat do .json s try/except pro vytvoření json při prvním způštění
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# NAJÍT HESLO #

def find_pass():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Chyba", message="Záznam nenalezen.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Chyba", message=f"Záznam pro web {website} nenalezen.")

# UI NASTAVENÍ#

window = Tk()
window.title("Pass Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=320, width=320)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(190, 190, image=logo_img)
canvas.grid(row=0, column=1)


# Popisky
website_label = Label(text="Website")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)
password_label = Label(text="Password")
password_label.grid(row=3, column=0)


# Vstupy
website_entry = Entry(width=30)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=30)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "libor.sehnal@gmail.com")
password_entry = Entry(width=30)
password_entry.grid(row=3, column=1)


# Tlačítka
generate_pass_button = Button(text="Generovat", command=generate_password)
generate_pass_button.grid(row=3, column=2)
add_button = Button(text="Uložit", width=43, command=uloz)
add_button.grid(row=4, column=1, columnspan=2)
generate_search_button = Button(text="Hledej", width=7, command=find_pass)
generate_search_button.grid(row=1, column=2)

window.mainloop()