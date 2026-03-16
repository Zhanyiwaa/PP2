import os

#1.create a single directory 
os.mkdir("test_dir")
print("created test_dir")

#2.create nested directories
os.makedirs("parent/child/grandchild",exist_ok=True)
print("created parent/child/grandchild directories")

#3.list all files and directories in current folder
print("all files/folders",os.listdir("."))

#4.find all .txt files in currrent folders
for file in os.listdir("."):
    if file.endswith(".txt"):
        print("txt file found:",file)

#5.show current working directory 
print("current directory:",os.getcwd())