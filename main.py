from tkinter import *
from tkinter import messagebox
import random
import json

RED = '#d4483b'
WHITE = '#ffffff'
FONT = ('roboto', 10, "normal")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    win = Toplevel()
    win.title("Generate Password")
    win.config(padx=20, pady=20)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '&', '(', ')', '@']

    # Labels
    title_label = Label(win, text="Customize your password", font=("Roboto", 18, "bold"))
    title_label.grid(row=1, column=1, columnspan=2)

    letters_label = Label(win, text="How many letters?", font=FONT)
    letters_label.grid(row=2, column=1)

    num_label = Label(win, text="How many numbers?", font=FONT)
    num_label.grid(row=3, column=1)

    symbol_label = Label(win, text="How many symbols?", font=FONT)
    symbol_label.grid(row=4, column=1)

    # Entries
    letters_entry = Entry(win)
    letters_entry.focus()
    letters_entry.grid(row=2, column=2)

    num_entry = Entry(win)
    num_entry.grid(row=3, column=2)

    symbol_entry = Entry(win)
    symbol_entry.grid(row=4, column=2)

    def generate_and_insert_password():
        try:
            password_letters = [random.choice(letters) for _ in range(int(letters_entry.get()))]
            password_symbols = [random.choice(symbols) for _ in range(int(symbol_entry.get()))]
            password_numbers = [random.choice(numbers) for _ in range(int(num_entry.get()))]
            password_list = password_letters + password_numbers + password_symbols

            random.shuffle(password_list)
            generated_password = "".join(password_list)

            password_entry.insert(0, generated_password)
            win.destroy()
        except ValueError:
            messagebox.showinfo(title="Error", message="Please don't leave any fields empty.")

    generate_btn = Button(win, text="Generate", command=generate_and_insert_password, width=20, bg=RED, fg=WHITE,
                          relief=FLAT)
    generate_btn.grid(row=5, column=1, columnspan=2, pady=3)

    win.mainloop()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    new_data = {
        website_entry.get(): {
            "Email": email_entry.get(),
            "Password": password_entry.get(),
        }
    }
    if len(website_entry.get()) == 0 or len(password_entry.get()) == 0 or len(email_entry.get()) == 0:
        messagebox.showwarning(title="Opps", message="Please don't leave any of the fields empty!")
    else:
        try:
            with open("data.json", "r") as file:
                # reading the old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # updating the old data with new data
            data.update(new_data)
            with open("data.json", "w") as file:
                # saving the updated data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as file:
            data_file = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data_file:
            messagebox.showinfo(title=website, message=f"Email: {data_file[website]['Email']} \nPassword: "
                                                       f"{data_file[website]['Password']}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Password Manager")
root.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=1, column=2)

# Labels
website_label = Label(text="Website/App:", font=FONT)
website_label.grid(row=2, column=1)

email_label = Label(text="Email/Username:", font=FONT)
email_label.grid(row=3, column=1)

password_label = Label(text="Password:", font=FONT)
password_label.grid(row=4, column=1)

# Entries

website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=2, column=2, sticky="EW", padx=2, pady=3)

email_entry = Entry(width=35)
email_entry.insert(0, "harshukaurbal@gmail.com")
email_entry.grid(row=3, column=2, columnspan=2, sticky="EW", padx=2, pady=3)

password_entry = Entry(width=21)
password_entry.grid(row=4, column=2, sticky="EW", padx=3, pady=3)

# Buttons
search_btn = Button(text="Search", command=find_password, bg=RED, fg=WHITE, relief=FLAT)
search_btn.grid(row=2, column=3, sticky="EW", padx=3, pady=3)

generate_password_btn = Button(text="Generate", command=generate_password, bg=RED, fg=WHITE, relief=FLAT)
generate_password_btn.grid(row=4, column=3, sticky="EW", padx=3, pady=3)

add_btn = Button(text="Add", width=36, command=save_data, bg=RED, fg=WHITE, relief=FLAT)
add_btn.grid(row=5, column=2, columnspan=2, pady=3)

root.mainloop()
