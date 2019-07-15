#!/usr/bin/python3
# coding=utf-8
'''
测试时mongodb数据库测试文件
'''
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient.voice_finger
myquery = {"name":"first_est"}
mydb = myclient.voice_finger
mycol = mydb.voice_finger

namecount = mycol.find()
# if namecount != None:
#     print("the song has been record!")
# else:
#     print("no")

for x in namecount:
    print(x.get('name'))
    # print("the song has been record")
    # return None

# mydict = {"name":"second_test","fp":"v.high_point.__str__()"}
# mycol.insert_one(mydict)