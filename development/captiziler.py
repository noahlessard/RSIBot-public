import json


def capitalize(x):
  return x.upper()


jsondata = open('new_ticker_data.json')
mainlist = json.load(jsondata)
newlist = []

for x in mainlist:
	newlist.append(capitalize(x))
jsondata.close()

print(newlist)

with open ('c.json', 'w') as f:
	json.dump(newlist, f)

