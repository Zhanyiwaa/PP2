# "r" - Read - Default value. Opens a file for reading, error if the file does not exist
# "a" - Append - Opens a file for appending, creates the file if it does not exist
# "w" - Write - Opens a file for writing, creates the file if it does not exist
# "x" - Create - Creates the specified file, returns an error if the file exists
# "t" - Text - Default value. Text mode
# "b" - Binary - Binary mode (e.g. images)

#1.Read whole file
with open ("data.txt","r") as f:
    print(f.read())

#2.Read line by line 
with open("data.txt","r") as f:
    for line in f:
        print(line.strip())

#3.Readline
with open("data.txt","r") as f:
    print(f.readline())
    print(f.readline())

#4.Readlines
with open("data.txt","r") as f:
    lines=f.readlines()
    print(lines)
#5.Count lines in file 
with open("data.txt","r") as f:
    lines=f.readlines()
    print(len(lines))