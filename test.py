import string

word = "user,name"
list = [*word]
check = string.ascii_letters + string.digits + "_" + "@" + "."
whitelist = [*check]


for i in list:
    if i in whitelist:
        pass
    else:
        print("error")