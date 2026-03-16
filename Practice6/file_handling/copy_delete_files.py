import shutil
import os

#1.copy file
shutil.copy("data.txt","copy.txt")

#2.copy file to folder
shutil.copy("data.txt","./copy2.txt")

#3.move file
shutil.move("data.txt","move.txt")

#4.delete file 
if os.path.exists("move.txt"):
    os.remove("move.txt")

#5.checking if file exists
print(os.path.exists("data.txt"))