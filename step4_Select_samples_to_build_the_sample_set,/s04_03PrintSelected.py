# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 10:31:57 2023

@author: panxinpower
"""

'''
输出被选择LabelName，需要在ArcGis中运行
'''

import numpy as np;
import os;
import pickle;
import re;
import copy;
import arcpy;


workspacename=r"K:\a-paper2023-gisdata\1-firstsamples\project\arcgisprojectsample\mysampleproject\mysampleproject.gdb";
fcname="jlobjectsall";
fields = ['SHAPE@','LableNumbe']

arcpy.env.workspace=workspacename;
fc=fcname;
cursor = arcpy.da.SearchCursor(fc, fields);
mydict=dict();
i=0;
for row in cursor:
    print(row[1],end=' ');