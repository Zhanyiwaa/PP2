#program to convert a given camel case string to snake case.
import re
s=input()
c=re.sub(r'([A-Z])',lambda x:'_'+ x.group(1).lower(),s)
print(c)