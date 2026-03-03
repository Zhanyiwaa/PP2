#program to replace all occurrences of space, comma, or dot with a colon.
import re
s=input()
r=re.sub(r'[ ,.]',':',s)
print(r)