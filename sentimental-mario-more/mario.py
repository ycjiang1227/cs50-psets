# TODO

#declarations
valid_num = False

# get height between 1 and 8 inclusive
while not valid_num:
    try:
        height = int(input("Height: "))
        if height > 0 and height <= 8:
            valid_num = True
    except:
        valid_num = False

# print pyramid of hashes
for x in range(1, height + 1):
    print(" "*(height-x) + "#"*x + "  " + "#"*x)