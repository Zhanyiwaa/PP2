#program to find sequences of lowercase letters joined with a underscore.
import re
s=input()
match=re.findall(r'[a-z]+_[a-z]+',s)
print(match)