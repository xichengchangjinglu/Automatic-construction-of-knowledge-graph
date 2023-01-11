# -*- encoding:utf-8 -*- 
from pprint import pprint
from paddlenlp import Taskflow
import pandas
import json

with open('json/affectedBody.json','r',encoding='utf8')as json_file:
    affectdeBody = json.load(json_file)
with open('json/causingFactor.json','r',encoding='utf8')as json_file:
    causingFactor = json.load(json_file)
with open('json/disasterBearingEnvironment.json','r',encoding='utf8')as json_file:
    disasterBearingEnvironment = json.load(json_file)
schema=[]
for list in affectdeBody.values():
    for index in range(0,len(list)):
        schema.append(list[index])
for list in causingFactor.values():
    for index in range(0,len(list)):
        schema.append(list[index])
for list in disasterBearingEnvironment.values():
    for index in range(0,len(list)):
        schema.append(list[index])
# print(schema)

ie = Taskflow('information_extraction', schema=schema)
file=pandas.read_excel('data\data.xlsx')
number=file.shape[0]
for i in range(0,3):
    sentence=file.loc[i][0]
    data=ie(sentence)
    filename="json/result"+str(i)+".json"
    with open(filename, 'a',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)
    

    