with open('csv/Tags.csv','r') as f:
    text = f.read()


import re

# text = re.sub(r"[^\x00-\x7F]+",r"", text)
text = re.sub(r"'",r"''", text)
tags = text.splitlines()
for i, name in enumerate(tags):
    if name == '' or len(name) > 250:
        tags.pop(i)
    else :
        tags[i] = name.strip()
tags = list(set(tags))
print(len(tags))

with open('../tags_wordlist.txt','w') as f:
    f.write('\n'.join(tags))