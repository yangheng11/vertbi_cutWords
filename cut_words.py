#encoding=utf-8
'''
维特算法分词应用
'''
#预料词典处理，将搜狗新闻预料库处理成频率预料库
import math
import re
import numpy as np
import os
def data_processing(path,save_path):
    #统计总词频
    total_freq=0
    file=open(path,"rb")
    lines=file.readlines()
    for line in lines:
        try:
            line=line.decode("gbk")
        except:
            continue
        item=line.split("\t")
        total_freq=total_freq+int(item[1])
    #计算词典中每个词的频率
    file1=open(save_path,"w",encoding="utf-8")
    for line in lines:
        try:
            line=line.decode("gbk")
            item = line.split("\t")
            file1.write(item[0]+"\t"+str(-math.log2(int(item[1])/total_freq))+"\n")
        except Exception as e :
            print(e)
            continue
import sys
sys.setrecursionlimit(100000) #例如这里设置为十万
def cut_sentence(sentence,sentences):
    '''
    将输入的句子按照符号分开
    :param sentence:
    :param sentences:
    :return:
    '''
    pattern = re.compile(u'[^\u4e00-\u9fa5]')
    sentences = sentences
    flag=True
    if len(pattern.findall(sentence))<1:
        flag=False
    if flag==True:
        seq_char=pattern.findall(sentence)[0]
        sentence_list=sentence.split(seq_char)
        for sentence1 in sentence_list:
            if pattern.findall(sentence1) or sentence1=="":
                sentences=cut_sentence(sentence1,sentences)
            elif sentence1!="":
                sentences.append(sentence1)
    return sentences
def get_minPath(graph,length,sentence,path,cut_words):
    #获去图中节点的个数,从后向前匹配
    length=length #途中最后一个节点的编号
    if length>=1:
        #获取推重到当前节点的所有路径
        start_node=[]
        path_length=[]
        for node in graph:
            if node["end"]==length:
                start_node.append(node["start"])
                path_length.append(node["prob_values"])
        assary_path=np.asanyarray(path_length)
        if assary_path.min() ==1000000:
            #词典中没有以该汉字结尾的词，默认分词为单个字符
            node_number=length-1
        else:
            node_number=start_node[path_length.index(assary_path.min())]
        path.append(node_number)
        path.append(length)
        cut_words.append(sentence[node_number:length])
        sentence = sentence[0:node_number]
        length = node_number
        path,cut_words=get_minPath(graph,length,sentence,path,cut_words)
    return path,cut_words
def cut_word(path_dic,sentence):
    cudir=os.path.abspath(".")
    print(cudir)
    path=cudir+"\\"+path_dic
    print(path,"path")
    file=open(path_dic,"r",encoding="utf-8")
    Prob_dic={}
    lines=file.readlines()
    for line in lines:
        item=line.split("\t")
        Prob_dic.setdefault(item[0],float(item[1].strip("\n")))
    #使用维特比算法进行分词
    #根据输入语句和词典构建图
    cut_words=[]
    sentences=cut_sentence(sentence,[])
    for sentence in sentences:
        #针对每个小距句自己进行分词，减小时间复杂度
        node = {}
        word_grahp = []
        path_node = [0]
        word_grahp.append({"start": -1, "end": 0, "prob_values": 0})
        #词典中不存在的的prob_value=100
        length=len(sentence)
        for i in range(len(sentence)+1):
            for j in range(i+1,len(sentence)+1):
                words=Prob_dic.keys()
                if sentence[i:j] in words:
                    word_grahp.append({"start":i,"end":j,"prob_values":Prob_dic[sentence[i:j]],"word":sentence[i:j]})
                else:
                    word_grahp.append({"start": i, "end": j, "prob_values": 1000000, "word":sentence[i:j]})
        #得到词汇之间的有向图，获去最短路径
        localpath,cut_words_child=get_minPath(word_grahp,length,sentence,[],[])
        cut_length=len(cut_words_child)
        #正向添加分析结果
        for i in range(cut_length):
            cut_words.append(cut_words_child[cut_length-i-1])
    return cut_words
print(cut_word("./Freq/SogouLabProb.txt",u"今天天气真好啊!我跟李明明说，我们去野外玩吧！小明说我要做作业。北京我爱你"))


