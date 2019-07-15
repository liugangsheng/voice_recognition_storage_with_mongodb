#!/usr/bin/python3
# coding=utf-8
'''
主程序
包含：添加歌曲函数 指纹比对函数 指纹搜索函数 指纹搜索并播放函数
'''
import os

import pymongo
import voice


class memory():
    def __init__(self, mongodb):
        '''
        初始化的方法，主要是存储连接数据库的参数
        :param mongodb: 数据库参数
        '''
        # mongodb参数初始化
        self.mongodb = "mongodb://localhost:27017/"

    def addsong(self, path):
        '''
        添加歌曲方法，将歌曲名和歌曲特征指纹存到数据库
        :param path: 歌曲路径
        :return:
        '''
        # 参数错误处理
        if type(path) != str:
            raise TypeError('path need string')

        basename = os.path.basename(path)

        # mongodb建立连接
        try:
            myclient = pymongo.MongoClient(host=self.mongodb)
        except:
            print('DataBase error')
            return None

        # mongodb查找歌曲名字
        myquery = {"name": basename}
        mydb = myclient.voice_finger
        mycol = mydb.voice_finger
        namecount = mycol.find(myquery)
        for x in namecount:
            print(basename + " the song has been record!")
            return None

        # 计算音频指纹
        v = voice.voice()
        v.loaddata(path)
        v.fft()

        # mongodb插入数据
        mydict = {"name": basename, "fp": v.high_point.__str__()}
        mycol.insert_one(mydict)

    def fp_compare(self, search_fp, match_fp):
        '''
        核心比对算法
        :param search_fp: 查询指纹
        :param match_fp: 库中指纹
        :return:最大相似值 float
        '''
        if len(search_fp) > len(match_fp):
            return 0
        max_similar = 0
        search_fp_len = len(search_fp)
        match_fp_len = len(match_fp)
        for i in range(match_fp_len - search_fp_len):
            temp = 0
            for j in range(search_fp_len):
                if match_fp[i + j] == search_fp[j]:
                    temp += 1
            if temp > max_similar:
                max_similar = temp
        return max_similar

    def search(self, path):
        '''
        搜索方法，输入为文件路径
        :param path: 待检索文件路径
        :return: 按照相似度排序后的列表，元素类型为tuple，二元组，歌曲名和相似匹配值
        '''
        # 参数错误处理
        if type(path) != str:
            raise TypeError('path need string')

        # 计算音频指纹
        v = voice.voice()
        v.loaddata(path)
        v.fft()
        # mongodb连接数据库
        try:
            myclient = pymongo.MongoClient(host=self.mongodb)
        except:
            raise IOError('DataBase error')

        # monogodb提取全部的指纹，出来进行比对
        compare_res = []
        mydb = myclient.voice_finger
        mycol = mydb.voice_finger
        for i in mycol.find():
            compare_res.append(
                (self.fp_compare(v.high_point[:-1], eval(i.get('fp'))), i.get('name')))
        compare_res.sort(reverse=True)
        print(compare_res)
        return compare_res

    def search_and_play(self, path):
        '''
        搜索方法顺带了播放方法
        :param path:文件路径
        :return:
        '''
        # 参数错误处理
        if type(path) != str:
            raise TypeError('path need string')

        # 计算音频指纹
        f = voice.voice()
        f.loaddata(path)
        f.fft()
        # mongodb连接数据库
        try:
            myclient = pymongo.MongoClient(host=self.mongodb)
        except:
            raise IOError('DataBase error')

        # monogodb提取全部的指纹，出来进行比对
        compare_res = []
        mydb = myclient.voice_finger
        mycol = mydb.voice_finger
        for i in mycol.find():
            compare_res.append(
                (self.fp_compare(f.high_point[:-1], eval(i.get('fp'))), i.get('name')))
        compare_res.sort(reverse=True)
        print(compare_res)
        # 播放
        f.play(compare_res[0][1])
        return compare_res


if __name__ == '__main__':
    sss = memory(mongodb="mongodb://localhost:27017/")

    # 添加歌曲
    sss.addsong('aohan.wav')
    sss.addsong('lvse.wav')
    sss.addsong('celian.wav')
    sss.addsong('xiaoxingyun.wav')
    sss.addsong('hongzhaoyuan.wav')

    # 查找并播放
    sss.search_and_play('record_hongzhaoyuan.wav')
