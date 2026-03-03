#program that matches a string that has an 'a' followed by two to three 'b'.
import re
s=input().strip()
if re.fullmatch(r'ab{2,3}',s):
    print("match")
else:
    print("no match")