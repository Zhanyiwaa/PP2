#program to find the sequences of one upper case letter followed by lower case letters.
import re
s=input()
match=re.findall(r'[A-Z][a-z]+',s)
print(match)