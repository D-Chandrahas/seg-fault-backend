import re
import pandas
from io import StringIO

only_tags = StringIO()

df = pandas.read_csv('csv/Tags.csv', encoding='utf-8', keep_default_na=False)
df = df['TagName']
df.to_csv(only_tags, encoding='utf-8', header=False, index=False)


text = only_tags.getvalue()

text = re.sub(r"[^\x00-\x7F]+",r"", text)
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

with open('../../database/tags.txt','w') as f:
    f.write('\n'.join(tags))