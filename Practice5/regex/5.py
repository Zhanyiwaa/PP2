#program that matches a string that has an 'a' followed by anything, ending in 'b'
import re
s=input().strip()
if re.fullmatch(r'a.*b$',s):
    print("match")
else:
    print("no match")
