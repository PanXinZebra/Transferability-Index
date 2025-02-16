# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 15:18:53 2023

@author: panxinpower
"""
import pickle as pk
import numpy as np;
#from pyproj import Transformer
from multiprocessing.pool import ThreadPool as Pool

#id 和位置文件
databasefile=r'K:\a-paper2023-gisdata\adataset\pdb.npy';

#s1文件, 里面有-50构成的空洞
databasefiles1=r'K:\a-paper2023-gisdata\adataset\pdbs1.npy';

#s1文件, 里面的-50空洞被填充了
databasefilesf1=r'K:\a-paper2023-gisdata\adataset\pdbsf1.npy';

#判断s1 paddy之后的结果
databasefilepaddy=r'K:\a-paper2023-gisdata\adataset\pdbpaddy.npy';

#所有外框
framefile=r'K:\a-paper2023-gisdata\adataset\frame.npy';

#2021年所有数据
sample2021allfile=r'K:\a-paper2023-gisdata\adataset\1sample.npy';



#2020年所有数据
sample2020allfile=r'K:\a-paper2023-gisdata\adataset\2sample.npy';

'''
//存储决策数据
原始数据，原始决策数据， 训练X，测试x, 训练6类目decsion，训练2类目decsion，测试6类目decsion，测试2类目decsion
'''
#数据集 2021
decsiondataset2021file=r'K:\a-paper2023-gisdata\adataset\decsiondataset2021.pkl'


#数据集 2020 仅仅用于测试  原始数据，原始决策数据， 所有数据， 所有决策7类目, 所有决策2类目
decsiondataset2020file=r'K:\a-paper2023-gisdata\adataset\decsiondataset2020.pkl'


#第二次重构的Decision
dbdecision2021file=r'K:\a-paper2023-gisdata\adataset\dbdecision2021.pkl'




def pdbloadsample2021all():
    temp=np.load(sample2021allfile,allow_pickle=True);
    return temp[0];

def pdbloadsample2020all():
    temp=np.load(sample2020allfile,allow_pickle=True);
    return temp[0];

def pdbloaddecsiondataset2021():
    file = open(decsiondataset2021file, 'rb')
    value=pk.load(file)
    file.close();
    return value;

def pdbloaddecsiondataset2020():
    file = open(decsiondataset2020file, 'rb')
    value=pk.load(file)
    file.close();
    return value;

def pdbloaddb2021():
    file = open(dbdecision2021file, 'rb')
    value=pk.load(file)
    file.close();
    return value;
    
    

def pdbload():
    temp=np.load(databasefile,allow_pickle=True);
    return temp[0];

def pdbloads1():
    temp=np.load(databasefiles1,allow_pickle=True);
    return temp[0];

def pdbloadsf1():
    temp=np.load(databasefilesf1,allow_pickle=True);
    return temp[0];

def pdbloadpaddy():
    temp=np.load(databasefilepaddy,allow_pickle=True);
    return temp[0];

def pdbloadframedb():
    temp=np.load(framefile,allow_pickle=True);
    return temp[0];


def pdbsave(pdb):
    np.save(databasefile,[pdb]);
    
def splitkeys(keys):
    list1=[];
    sublist=[];
    num=1499;
    i=0;
    for item in keys:
        sublist.append(item);
        if (i<num):
            i=i+1;
        else:
            list1.append(sublist);
            sublist=[];
            i=0;
        
    if (len(sublist)!=0):
        list1.append(sublist);
        
    numsum=0;
    for elist in list1:
        numsum=numsum+len(elist);
    print("Split into %d sublists and overall item is %d"%(len(list1),numsum));
    '''
    i=0;
    for ekey in pdb.keys():
        i=i+1;
    print(i);
    '''    
    return list1;
        
    
def pdb4326to3857(pdb):
   
    #必须指定always_xy=True，否则投影转换时就得先纬度后精度，这不符和常规习惯
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857",always_xy=True)
    def runitems(items):
        for item in items:
            pass;
            values=pdb[item];
            LX=values['X'];
            LY=values['Y'];
            
            PX,PY=transformer.transform(LX, LY)
            values['PX']=PX;
            values['PY']=PY;
            
    keylist=splitkeys(pdb.keys());
    pool = Pool(13);
    i=0;
    for items in keylist:
        pool.apply(runitems, (items,))
        print("Process %d"%(i));
        i=i+1;
        
    pool.close();
    pool.join();      

#单线程版本
def pdb4326to3857Normal(pdb):
    #必须指定always_xy=True，否则投影转换时就得先纬度后精度，这不符和常规习惯
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857",always_xy=True)
    i=0;
    for item in pdb.keys():
        values=pdb[item];
        LX=values['X'];
        LY=values['Y'];
        PX,PY=transformer.transform(LX, LY)
        PXT=values['PX'];
        PYT=values['PY'];
        ttvv=abs(PXT-PX)+abs(PYT-PY);
        if (ttvv>0.001):
            print(item);
        
        values['PX']=PX;
        values['PY']=PY;
        i=i+1;
        if (i%1000==0):
            print(i);

#pdb=pdbload();

#framedb=pdbloadframedb();
#pdbs1=pdbloads1();
#pdbsf1=pdbloadsf1();
#pdbpaddy=pdbloadpaddy();

#sample2021all=pdbloadsample2021all();
#sample2020all=pdbloadsample2020all();


#pdbdecsiondataset2021=pdbloaddecsiondataset2021();
#pdbdecsiondataset2020=pdbloaddecsiondataset2020();


#dbdecision2021=pdbloaddb2021();
# 计算3857投影
#pdb4326to3857Normal(pdb);
#for key in pdb.keys():
#    print(pdb[key])
#    break;
#pdbsave(pdb);




    
    
    
    
    
    
    
    
    
    

    