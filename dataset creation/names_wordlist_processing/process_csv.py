with open('csv/Users.csv','r',encoding='utf-8') as f:
    text = f.read()


import re

text = re.sub(r"[^\x00-\x7F]+",r"", text)
text = re.sub(r"'",r"''", text)
names = text.splitlines()
for i, name in enumerate(names):
    if name == '' or len(name) > 250:
        names.pop(i)
    else :
        names[i] = name.strip()
names = list(set(names))
print(len(names))

with open('../names_wordlist.txt','w') as f:
    f.write('\n'.join(names))