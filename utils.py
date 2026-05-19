import secrets
import string
import tkinter as tk

uppercase = string.ascii_uppercase
lowercase = string.ascii_lowercase
numbers   = string.digits
symbols   = string.punctuation
letters = uppercase + lowercase + numbers + symbols

def generate_password(length):
    passwd = []
    passwd.append(secrets.choice(uppercase))
    passwd.append(secrets.choice(lowercase))
    passwd.append(secrets.choice(numbers))
    passwd.append(secrets.choice(symbols))
    for i in range(length -4):
        passwd.append(secrets.choice(letters))
    secrets.SystemRandom().shuffle(passwd)
    return "".join(passwd)



def copy_to_clipboard(text):
    root=tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
  