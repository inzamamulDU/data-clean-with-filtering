import os

whitelist_file = open("botnet_match.txt", "r")
bad_words = whitelist_file.read().splitlines()
whitelist_file.close()

with open("botnet.host.dtq", "r") as a_file :
    lines = a_file.readlines()
    for num,line in enumerate(lines,1):
        print("hello")
                    #line = filename.readlines()
        for word in bad_words:
            if word in line:
                print(num)
                del lines[num-2:num+2]


os.remove("botnet.host.dtq")
print("File Removed!")
new_file = open("botnet.host.dtq", "w+")

for line in lines:
    new_file.write(line)

new_file.close()
