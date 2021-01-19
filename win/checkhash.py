import hashlib
import sys

r'''
Make sure the file check_hash.py is in the path.
Then run the given reg file


'''
hsh = input("Enter hash type:") or "sha256"
functions = {
    'sha256':hashlib.sha256,
    'sha512':hashlib.sha512,
    'md5':hashlib.md5,
    'sha3_512':hashlib.sha3_512,
    'sha3_256':hashlib.sha3_256,
}

with open(sys.argv[1], "rb") as f:
    file_hash = functions.get(hsh.lower(), None)
    if file_hash is None:
        print("Warning: Required hash type not found ... choosing sha256")
        file_hash = functions.get('sha256')()
    else:
        file_hash = file_hash()
    while chunk := f.read(8192):
        file_hash.update(chunk)

fhash = file_hash.hexdigest()

print(f"{hsh}:{fhash}")
inp = input("Enter the correct hash:")
if inp == fhash:
    print("Hash verified! Correct")

else:
    print("Hash verification failed! Incorrect")

i = input()