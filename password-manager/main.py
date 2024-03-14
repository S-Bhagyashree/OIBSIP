from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generates a random password based on the secure password standards:
    8-10 alphabets
    2-4 numbers
    2-4 symbols
    Displays the generated password on the UI and copies the 
    generated password to the clipboard.
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
               'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 
               'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pass_letters = [choice(letters) for _ in range(randint(8,10))]
    pass_numbers = [choice(numbers) for _ in range(randint(2,4))]
    pass_symbols = [choice(symbols) for _ in range(randint(2,4))]

    password_list = pass_letters + pass_symbols + pass_numbers
    shuffle(password_list)
    password_text = "".join(password_list)
    password.insert(0, password_text)
    pyperclip.copy(password_text) # to copy to the clipboard

# ---------------------------- SAVE PASSWORD ------------------------------- #
def update_file(entry, file_name = "data.json"):
    """Function takes the entry to be added to the json file with website, username, 
    and password details.

    Args:
        entry (dict): Entry should have the format {website: {username:"", password:""}}
        file_name (str, optional): JSON file (our datafile). Defaults to "data.json".
    """
    with open(file_name, "w", encoding = 'utf-8') as f:
        json.dump(entry, f, indent = 4)

def save():
    """Procures the website, username/email, and password entered by the user on UI. 
    Then updates the entered information to the JSON data file. If it's the first enrty, 
    exist then it creates the file.
    If the entries are blank then prompts the user to make valid entries and 
    prompts the user to verify the entered information before actually updating the data file.
    After updates, erases the entered information from UI to get ready to accept new entries.
    """
    web_entry = website.get()
    uname_entry = uname.get()
    pass_entry = password.get()
    new_entry = {
        web_entry: {
            'username': uname_entry,
            'password': pass_entry
        }
    }
    if len(web_entry)==0 or len(pass_entry)==0:
        messagebox.showinfo(title="Oops...",
                             message = "Please make sure you have entered the correct details.")
    else:
        is_ok = messagebox.askokcancel(title = web_entry,
                            message =f"These are the details entered: \nUsername: {uname_entry}"
                            f"\nPassword: {pass_entry} \nProceed to save?")
        if is_ok:
            try:
                with open("data.json", "r", encoding = 'utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                update_file(new_entry)
            else:
                data.update(new_entry)
                update_file(data)
            finally:
                website.delete(0, END)
                password.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    """Function captures the website entry and prompts to the user the username and password 
    after procuring it from the data file. 
    It the data file does not exist prompts user to first add entries to create a file before 
    searching.
    If the website is not in the datafile, prompts the user that the website does not exist 
    in the datafile.
    """
    web_entry = website.get()
    try:
        with open("data.json", "r", encoding = 'utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops....",
                            message="File does not exist.\
                                \nPlease add details to create a file before you search.")
    else:
        try:
            entries = data.get(web_entry)
            messagebox.showinfo(title= web_entry,
                                message=f"email/uname: {entries['username']}\
                                    \npassword: {entries['password']}")
        except TypeError:
            messagebox.showinfo(title="Error", message=f"Details for the {web_entry} not found.\
                \nPlease, ensure you have entered the correct website.")
        finally:
            f.close()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config( padx = 50, pady = 50)

canvas = Canvas(width = 200, height = 200)
logo_img = PhotoImage(file = "logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column = 1, row =0)

label1 = Label(text="Website:")
label1.grid(column=0, row = 1)

website = Entry(width = 35)
website.grid(column=1, row = 1, columnspan = 2, sticky= 'w')

search = Button(text="Search", command=search_password)
search.grid(column = 2, row = 1)

label2 = Label(text="Email/Username:")
label2.grid(column = 0, row = 2)

uname = Entry(width = 35)
uname.grid(column = 1, row = 2, columnspan  =2, sticky = 'w')

label3 = Label(text = "Password:")
label3.grid(column = 0, row  =3)

password  = Entry(width = 21)
password.grid(column = 1, row  =3, sticky = 'w')

gen_pass  = Button(text="Generate Password", command = generate_password)
gen_pass.grid(column = 2, row = 3)

add = Button(text="Add", width = 36, command = save)
add.grid(column = 1, row = 4, columnspan = 2, sticky  ='w', pady = 10)

window.mainloop()
