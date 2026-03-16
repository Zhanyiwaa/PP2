#1.write text
with open("data.txt","w") as f:
    f.write("Hello Python\n")

#2.write multiple lines
with open("data.txt","w") as f:
    f.write("line1\n")
    f.write("line2\n")

#3.append text
with open("data.txt","a") as f:
    f.write("new appended line\n")

#4.write list of strings
lines=["apple\n",'banana','cherry']
with open("data.txt","w") as f:
    f.writelines(lines)

#5.create file with x mode
with open("data.txt","x") as f:
    f.write("file with x mode")