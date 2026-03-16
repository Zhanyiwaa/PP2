import shutil
import os

#1.move a file into a folder
os.makedirs("back_up",exist_ok=True)
shutil.move("data.txt","backup/data.txt")
print("moved data.txt to backup/")

#2.copy file back to directory 
shutil.copy("backup/data.txt","data_copy.txt")
print("copied data.txt as data_copy.txt")

#3.rename file
os.rename("data_copy.txt","renamed_data.txt")
print("renamed data_copy.txt as renamed_data.txt")

#4.move file into nested folder 
os.makedirs("parent/child",exist_ok=True)
shutil.move("renamed_data.txt","parent/child_renamed_data.txt")
print("moved renamed_data.txt to parent/child/")

#5.list contens of nested folder
print("files in parent/child",os.listdir("parent/child"))