from gettext import translation
from hmac import trans_36


with open("./trans.txt", "r") as r, open("./trans_raw.txt","w") as w:
    for line in r:
        items = line.split(" ")
        if len(items)==2:
            w.write(items[1].strip()+"\n")
