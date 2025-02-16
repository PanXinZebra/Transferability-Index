# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:08:34 2023

@author: panxinpower
"""


import numpy as np;

#原始数据中有好多-50的洞，这个程序就是填充那个洞用的。全是-50的做成-30水面
#然后存储到databasefilesf1之中

def fillHole(a1):
    pass;
    datavalue=np.array(a1);
    
    for ii in range(4):
        d1=datavalue[ii*12:ii*12+12];   
        kk=np.where(d1<-49);
        avgvalue=np.mean(d1[np.where(d1>-49)]);
        
        nanvalue=False;
        if (np.isnan(avgvalue)):
            #直接做成“水面”尽量不影响程序决策
            avgvalue=-31;
            nanvalue=True;
            print("All data is -50");
            
        
        for ekk in kk[0]:
            pos1=ekk-1;
            pos2=ekk+1;
            value1=avgvalue;
            value2=avgvalue;
            if (pos1>=0):
                while (pos1>=0 and d1[pos1]<-49):
                    pos1=pos1-1;
                if (pos1>=0):
                    value1=d1[pos1];
                    
            if (pos2<=11):
                while (pos2<=11 and d1[pos2]<-49):
                    pos2=pos2+1;
                if (pos2<=11):
                    value2=d1[pos2];
            d1[ekk]=(value1+value2)/2.0
        
        if (nanvalue):
            print(datavalue.tolist());
                
        
    return datavalue.tolist();
    
    
    
    
i=0;

for ek in pdbs1.keys():
    value=pdbs1[ek];
    a1=value['s1data'];
    a2=fillHole(a1);
    value['s1data']=a2;
    i=i+1;
    if (i%10000==0):
        print(i);
        
np.save(databasefilesf1,[pdbs1]);
    

    
    