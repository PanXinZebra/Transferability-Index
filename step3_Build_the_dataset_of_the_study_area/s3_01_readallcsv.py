# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 08:41:46 2023

@author: panxinpower
"""

import pandas as pd
import numpy as np
import os

'''
读取所有哨兵1的csv数据并存盘
'''

filepath="K:\\a-paper2023-gisdata\\csvfile\\";

files=os.listdir(filepath);

pdbs1=pdb;

if a1 is None:
    print('isNone');
else:
    print(a1)

fieldname=['Y2018N00', 'Y2018N01', 'Y2018N02', 'Y2018N03', 'Y2018N04', 'Y2018N05', 'Y2018N06', 'Y2018N07', 'Y2018N08', 'Y2018N09', 'Y2018N10', 'Y2018N11', 'Y2019N00', 'Y2019N01', 'Y2019N02', 'Y2019N03', 'Y2019N04', 'Y2019N05', 'Y2019N06', 'Y2019N07', 'Y2019N08', 'Y2019N09', 'Y2019N10', 'Y2019N11', 'Y2020N00', 'Y2020N01', 'Y2020N02', 'Y2020N03', 'Y2020N04', 'Y2020N05', 'Y2020N06', 'Y2020N07', 'Y2020N08', 'Y2020N09', 'Y2020N10', 'Y2020N11', 'Y2021N00', 'Y2021N01', 'Y2021N02', 'Y2021N03', 'Y2021N04', 'Y2021N05', 'Y2021N06', 'Y2021N07', 'Y2021N08', 'Y2021N09', 'Y2021N10', 'Y2021N11', ];
indexname=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, ];


for file in files:
    filename=filepath+file;
    print(filename);
    
    df = pd.read_csv(filename);
    [hss,lss]=df.shape
    
    missfield=False;
    
    for row in range(hss):
        lable=df.loc[row][1]
        data=[]
        for i in indexname:
            currentfield=fieldname[i];
            gvalue=df.loc[row].get(currentfield);
            if gvalue is None:
                value=np.float64(-50.0);
                missfield=True;
            else:
                value=gvalue;
                
            if pd.isna(value):
                value=np.float64(-50.0);
            data.append(value);
        focusrow=pdbs1[lable];
        focusrow['s1data']=data;
        
    if missfield:
        print("---MissField");

databasefile=r'I:\a-paper2023-gisdata\adataset\pdbs1.npy';
np.save(databasefile,[pdbs1]);

for key in pds1.keys():
    aaavvv=pds1[key];
    break;
            