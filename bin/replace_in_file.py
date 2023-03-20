import sys

print(sys.argv)
args = sys.argv

with open(args[1], 'r') as file:
    filedata = file.read()
    filedata = filedata.replace(args[2], args[3])

with open(args[1], 'w') as file:
    file.write(filedata)

print(filedata)
print("Done")
