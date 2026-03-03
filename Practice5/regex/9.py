#program to insert spaces between words starting with capital letters.
import re
s=input()
r=re.findall(r'[A-Z][a-z]*',s)
w=" ".join(r)
print(w)