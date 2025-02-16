# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 14:45:49 2023

@author: panxinpower
"""



import numpy as np;
import os;
import pickle;
import re;
import copy;
import arcpy;
import numpy as np;

'''
write into arcgis
'''

[results]=np.load('K:\\a-paper2023-gisdata3\\adataset\\decision\\mymodel.npy',allow_pickle=True);
thename='tindex';
# tindex is field name



workspacename=r"K:\a-paper2023-gisdata3\arcgisprojectsample\mysampleproject\mysampleproject.gdb";
fcname="clxdata1";
fields = ['SHAPE@','LableNumbe',thename+'d18',thename+'d19',thename+'d20',thename+'d21'];
# Field names divided by year, such as "tindexd2021" indicates the result for the year 2021.

arcpy.env.workspace=workspacename;
fc=fcname;


cursor=arcpy.da.SearchCursor(fc, fields);

i=0;


with arcpy.da.UpdateCursor(fc, fields) as cursor:
    i=0;
    for row in cursor:
        pass;
        LableNumbe=row[1]; 
        arow=results[LableNumbe];
       
        row[2]=arow['d2018'];
        row[3]=arow['d2019'];
        row[4]=arow['d2020'];
        row[5]=arow['d2021'];

        cursor.updateRow(row);

        i=i+1;
        if (i%1000==0):
            print(i);


            
print("OK");

            
