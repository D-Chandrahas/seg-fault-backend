import re
import pandas
from io import StringIO

only_users = StringIO()

df = pandas.read_csv('csv/Users.csv', encoding='utf-8')
df = df['DisplayName']
df.to_csv(only_users, encoding='utf-8', header=False, index=False)

text = only_users.getvalue()

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