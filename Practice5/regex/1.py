#program that matches a string that has an 'a' followed by zero or more 'b''s.
import re
s=input().strip()
if re.fullmatch(r'ab*',s):
    print("match")
else:
    print("no match")