import json
from collections import defaultdict

people=['死亡','失踪','受伤','轻伤','重伤','受灾人数']
building=['房屋损坏','房屋倒塌','损坏','倒塌']
agriculture=['农作物','受灾面积','万公顷','公顷','绝收','亩','千亩','万亩']
economy=['经济损失','元','万元','亿元']
area=['地区']
affectedBody=defaultdict(list)
for i in range(0,len(people)-1):
    affectedBody['人口'].append(people[i])
for i in range(0,len(building)-1):
    affectedBody['房屋'].append(building[i])
for i in range(0,len(agriculture)-1):
    affectedBody['农业'].append(agriculture[i])
for i in range(0,len(economy)-1):
    affectedBody['经济'].append(economy[i])
for i in range(0,len(area)-1):
    affectedBody['地区'].append(area[i])    
# print(affectedBody)

typhoonFactor=['台风名称','灾害','致灾因子','台风']
causingFactor=defaultdict(list)
for i in range(0,len(typhoonFactor)-1):
    causingFactor['致灾因子'].append(typhoonFactor[i])
# print(causingFactor)  

typhoonEnvironment=['风速','风力','时间','东经','北纬','降雨','半径','大风级数']
disasterBearingEnvironment=defaultdict(list)
for i in range(0,len(typhoonEnvironment)-1):
    disasterBearingEnvironment['孕灾环境'].append(typhoonEnvironment[i])
# print(disasterBearingEnvironment)

with open('json/affectedBody.json', 'w',encoding='utf-8') as f:
    json.dump(affectedBody,f,ensure_ascii=False)
with open('json/causingFactor.json', 'w',encoding='utf-8') as f:
    json.dump(causingFactor,f,ensure_ascii=False)
with open('json/disasterBearingEnvironment.json', 'w',encoding='utf-8') as f:
    json.dump(disasterBearingEnvironment,f,ensure_ascii=False)