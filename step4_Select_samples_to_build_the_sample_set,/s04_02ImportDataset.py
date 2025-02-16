# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:58:18 2023

@author: panxinpower
"""

import psycopg2

conn = psycopg2.connect(database = "paper2023", user = "postgres", password = "panxin", host = "192.168.1.111", port = "5432");
print("Opened database successfully");



databasefilepaddy=r'K:\a-paper2023-gisdata\adataset\pdbpaddy.npy';

def pdbloadpaddy():
    temp=np.load(databasefilepaddy,allow_pickle=True);
    return temp[0];

pdbpaddy=pdbloadpaddy();

i=0;
conn.rollback();
cur = conn.cursor()

for ekey in pdbpaddy.keys():
    
 
    arow=pdbpaddy[ekey];
    
    mystr=''
    tvalue=arow['s1data'];
    for j in range(48):
        mystr=mystr+ ('%0.2f\t'%tvalue[j]);
        
    sql="Insert into objects values("+str(ekey)+", '"+mystr+"')";
    cur.execute(sql);
    
    i=i+1;
    if (i%1000==0):
        print(i);
        #conn.commit();
        
conn.commit();


conn.close()
print("OK");