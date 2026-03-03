#program to convert snake case string to camel case string.
import re
s=input()
c=re.sub(r'_([a-z])',lambda x: x.group(1).upper(),s)
print(c)
