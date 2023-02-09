with open('csv/Tags.csv','r') as f:
    text = f.read()


import re

# text = re.sub(r"[^\x00-\x7F]+",r"", text)
text = re.sub(r"'",r"''", text)
names = text.splitlines()
for i, name in enumerate(names):
    if name == '' or len(name) > 250:
        names.pop(i)
    else :
        names[i] = name.strip()
text = list(set(text))
print(len(names))

with open('../tags_wordlist.txt','w') as f:
    f.write('\n'.join(names))