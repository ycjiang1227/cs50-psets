from cs50 import get_string

# prompt for text
text = get_string("Text: ")

# initiate variables
letters = 0
sentences = 0
words = 1

for i in text:
    if i.isalpha():
        letters += 1
    elif i == " ":
        words += 1
    elif i == "." or i == "!" or i == "?":
        sentences += 1

# coleman-liau index
l = (letters / words) * 100
s = (sentences / words) * 100


def index(l, s):
    index = 0.0588 * l - 0.296 * s - 15.8
    return index


clindex = index(l, s)

# print results
if clindex < 1:
    print("Before Grade 1")
elif clindex > 16:
    print("Grade 16+")
else:
    print(f"Grade {round(clindex)}")