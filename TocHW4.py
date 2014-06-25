# -*- coding: utf-8 -*-
import sys
import urllib2
import json
import re

def getDataFromURL( url ):
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	data = response.read()
	data = json.loads(data)
	return data

# DEBUG
def checkPattern(d, ptn):
	for i in range(len(d)):
		result = re.match(ptn, data[i][roadHead])
		if result:
				matchData.add(d[i][roadHead][:result.start()+3])
	cnt = 0
	for i in matchData:
		cnt = cnt + 1
		print cnt, i

# find target in a list
def findAndAdd(lists, road, date, minPrice, maxPrice):
	for detail in lists:
		if detail['road'] == road:
			detail['date'].add(date)
			if minPrice < detail['minPrice']:
				detail['minPrice'] = minPrice
			if maxPrice > detail['maxPrice']:
				detail['maxPrice'] = maxPrice
			return
	s = set()
	s.add(date)
	tmp = {'road':road, 'date':s, 'minPrice':minPrice, 'maxPrice':maxPrice}
	lists.append(tmp)
	return

#URL = 'http://www.datagarage.io/api/5365dee31bc6e9d9463a0057'
# case I
#URL = 'http://www.datagarage.io/api/538447a07122e8a77dfe2d86'
# case II
#URL = 'http://www.datagarage.io/api/5384489ae7259bb37d9238d8'
# case III
URL = 'http://www.datagarage.io/api/5385b69de7259bb37d925971'
# case IV
#URL = 'http://www.datagarage.io/api/5385b858e7259bb37d926912'
data = getDataFromURL( URL )

regionHead = unicode('鄉鎮市區', 'utf-8')
roadHead = unicode('土地區段位置或建物區門牌', 'utf-8')
yearHead = unicode('交易年月', 'utf-8')
priceHead = unicode('總價元', 'utf-8')

#region = sys.argv[2] #'文山區'
#road = sys.argv[3] #'辛亥路'
#year = sys.argv[4] #'103'

region = unicode('文山區', 'utf-8')
road = unicode('臺北市中正區汀州路' , 'utf-8')
year = unicode('103', 'utf-8')
pattern = unicode('[路街巷]', 'utf-8')

patternR = unicode('[路街]', 'utf-8')
patternB = unicode('大道', 'utf-8')
patternA = unicode('[巷]', 'utf-8')

matchData = []

#checkPattern(data,unicode('[臺]', 'utf-8'))
cnt = 0
for i in range(len(data)):
	# Road, Boulevard, Alley
	resultR = re.search(patternR, data[i][roadHead])
	resultB = re.search(patternB, data[i][roadHead])
	resultA = re.search(patternA, data[i][roadHead])
	tmpRoad = ''
	if resultR:
		tmpRoad = (data[i][roadHead][:resultR.start()+1])
	elif resultB:
		tmpRoad = (data[i][roadHead][:resultB.start()+2])
	elif resultA:
		tmpRoad = (data[i][roadHead][:resultA.start()+1])
	if len(tmpRoad)>0:
		tmpDate = data[i][yearHead]
		tmpPrice = data[i][priceHead]
		findAndAdd(matchData,tmpRoad,tmpDate,tmpPrice,tmpPrice)


cnt = 0
max_dist_mth = 0
index = []
for i in range(len(matchData)):
	cnt = cnt + 1
	if len(matchData[i]['date']) > max_dist_mth:
		max_dist_mth = len(matchData[i]['date'])
		index = [i]
	elif len(matchData[i]['date']) == max_dist_mth:
		index.append(i)



for i in index:
#print i, matchData[i]['road'], len(matchData[i]['date']), matchData[i]['maxPrice'], matchData[i]['minPrice']
	print matchData[i]['road'], matchData[i]['maxPrice'], matchData[i]['minPrice']
