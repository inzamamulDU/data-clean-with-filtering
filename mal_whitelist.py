import os

whitelist_file = open("/var/sftp/files/mal.txt", "r")
bad_words = whitelist_file.read().splitlines()
whitelist_file.close()

with open("/tmp/toyo/spamhouse-data-clean/malware_domains.txt", "r") as a_file :
    lines = a_file.readlines()
    for num,line in enumerate(lines,1):
        print("hello")
                    #line = filename.readlines()
        for word in bad_words:
            if word in line:
                print(num)
                del lines[num-1]


os.remove("/tmp/toyo/spamhouse-data-clean/malware_domains.txt")
print("File Removed!")
new_file = open("/tmp/toyo/spamhouse-data-clean/malware_domains.txt", "w+")

for line in lines:
    new_file.write(line)

new_file.close()
