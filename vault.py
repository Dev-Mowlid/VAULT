import os 
import json
from cryptography.fernet import Fernet
from auth import derive_key

VAULT_FILE = "vault.json"

def load_vault(passwd):
    key = derive_key(passwd)
    fer = Fernet(key)

    try:
        with open(VAULT_FILE, "rb") as f:
            contents = f.read()
            decrepted = fer.decrypt(contents)
            json_strings = decrepted.decode()
            entries = json.loads(json_strings)
            return entries
    except FileNotFoundError:
        return []

def save_vault(passwd, entries):
    key = derive_key(passwd)
    fer = Fernet(key)

    json_strings = json.dumps(entries)
    encoded = json_strings.encode()
    encrypted = fer.encrypt(encoded)

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)
    

def add_entry(passwd, service, username, password):

    entries = load_vault(passwd)
    entries.append({"service":service, "username": username, "password":password})
    save_vault(passwd, entries)


def delete_entry(passwd, index):

    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError(f"Index must be integer, got {type(index).__name__}.")

    entries = load_vault(passwd)
    if index < 0 or index >= len(entries):
        raise IndexError(f"Index {index} is out of range, vault has {len(entries)} entries.")

    del entries[index]
    save_vault(passwd, entries)
    
def get_all_entries(passwd):
    return load_vault(passwd)
