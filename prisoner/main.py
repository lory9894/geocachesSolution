import json

with open('object.json') as f:
  data = json.load(f)

filestring = ""

for value in data:
    filestring += value

normalhex =""
for line in filestring.splitlines():
    for word in line.split():
        if len(word) == 4:
            normalhex += word[2:]
            normalhex += word[:2]
        else:
            normalhex += word
        normalhex += " "
    normalhex=normalhex[:-1]
    normalhex += "\n"

with open('object.hex', 'w') as f:
    f.write(normalhex)