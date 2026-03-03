#program to split a string at uppercase letters.
import re
s=input().strip()
m=re.findall(r'[A-Z][a-z]*',s)
print(m)

