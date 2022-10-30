import json
from collections import OrderedDict

jsondata = open('captial_ticker_data.json')
mainlist = json.load(jsondata)
print('orginal list length from captial ticker data', len(mainlist))

textdata = open('ftpdata')
oldtextlist = textdata.readlines()
newtextlist = []

for line in oldtextlist:
		newtextlist.append(line[:line.index('|')])
		mainlist.append(line[:line.index('|')])

print('orginal list length from ftpdata', len(newtextlist))
print('main list before sorting', len(mainlist))

finallist = list(OrderedDict.fromkeys(mainlist))

print('mainlist after sorting', len(finallist))

with open ('7000.json', 'w') as f:
	json.dump(finallist, f)
