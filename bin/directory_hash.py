import os
import hashlib
import sys

args = sys.argv


def sha256sum(filename):
    with open(filename, 'rb', buffering=0) as file:
        return hashlib.file_digest(file, 'sha1').hexdigest()


def hash_dir(dir_path):
    hashes = []
    for path, dirs, files in os.walk(dir_path):
        for file in sorted(files):  # we sort to guarantee that files will always go in the same order
            hashes.append(sha256sum(os.path.join(path, file)))
        for dir in sorted(dirs):  # we sort to guarantee that dirs will always go in the same order
            hashes.append(hash_dir(os.path.join(path, dir)))
        break  # we only need one iteration - to get files and dirs in current directory
    h = hashlib.new('sha1')  # sha256 can be replaced with diffrent algorithms
    h.update(''.join(hashes).encode())  # give a encoded string. Makes the String to the Hash
    return str(h.hexdigest())


def hahdir_as_int(directory):
    checksum = hash_dir(directory)
    price = int(''.join(filter(str.isdigit, checksum)))
    return price


checksum = hahdir_as_int(args[1])
print(checksum)
