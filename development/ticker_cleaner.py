import json
from collections import OrderedDict

orgjsondata = open('7000.json')
org = json.load(orgjsondata)

failedjsondata = open('failedlist.json')
fail = json.load(failedjsondata)

print(len(fail))
print(len(org))
org.extend(fail)
print(len(org))


finallist = [i for i in org if i not in fail]
print(len(finallist))


with open ('cleaned_7000.json', 'w') as f:
	json.dump(finallist, f)
