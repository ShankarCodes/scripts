#!/usr/bin/env python3
import hashlib
import sys
import tkinter as tk

functions = {
    # Add your functions here.
    'sha1':hashlib.sha1,
    'sha256':hashlib.sha256,
    'sha512':hashlib.sha512,
    'md5':hashlib.md5,
    'sha3_512':hashlib.sha3_512,
    'sha3_256':hashlib.sha3_256,
}

def make_text(label, content, master):
    text = tk.Text(master, height=1, borderwidth=0)
    text.insert(1.0, f"{label:<10} {content}")
    text.pack()
    text.configure(state="disabled")
    text.configure(inactiveselectbackground=text.cget("selectbackground"))
    return text


def main():
    print(sys.argv)
    master = tk.Tk()
    error = None
    if len(sys.argv) > 1:
        error = None
    else:
        error = "Please specify file name"

    if error is  None:
        hashers = [functions.get(func)() for func in functions]

        with open(sys.argv[1], "rb") as f:
            while chunk := f.read(8192):
                for hasher in hashers:
                    hasher.update(chunk)
        final_hsh = [hasher.hexdigest() for hasher in hashers]
        for func, hsh in zip(functions, final_hsh):
            make_text(func, hsh, master)
        
    else:
        make_text("Error", "Specify file name", master)
    tk.mainloop()

if __name__ == '__main__':
    main()
"""

r'''
Make sure the file check_hash.py is in the path.
Then run the given reg file


'''
print("Shankar Hash verifier")
print("(C) Shankar 2020")

try:
    import colorama
    colorama.init()

    
    red = colorama.Fore.RED
    yellow = colorama.Fore.YELLOW
    green = colorama.Fore.GREEN
    white = colorama.Fore.WHITE
    mag = colorama.Fore.MAGENTA

    sym = f"[*]"
except Exception as e:
    print("Unable to start color")
    sym = "[*]"
    red = yellow = green = white = mag =  ""


hsh = input(f"{sym}Enter hash type:") or "sha256"
functions = {
    # Add your functions here.
    'sha256':hashlib.sha256,
    'sha512':hashlib.sha512,
    'md5':hashlib.md5,
    'sha3_512':hashlib.sha3_512,
    'sha3_256':hashlib.sha3_256,
}

with open(sys.argv[1], "rb") as f:
    file_hash = functions.get(hsh.lower(), None)
    if file_hash is None:
        print(f"{sym} {yellow}Warning: Required hash type not found ... choosing sha256")
        file_hash = functions.get('sha256')()
    else:
        file_hash = file_hash()
    while chunk := f.read(8192):
        file_hash.update(chunk)

fhash = file_hash.hexdigest()

print(f"{sym} {mag}{hsh}:{fhash}")
inp = input(f"{sym} Enter the correct hash:")
if inp == fhash:
    print(f"{sym} {green}Hash verified! Correct")

else:
    print(f"{sym} {red}Hash verification failed! Incorrect")

i = input()
"""
