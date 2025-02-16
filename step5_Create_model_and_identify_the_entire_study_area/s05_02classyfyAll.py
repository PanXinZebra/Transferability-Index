# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:21:16 2023

@author: panxinpower
"""


pid=np.zeros((1075787),dtype='int');  
pv=np.zeros((1075787*4,12),dtype='float');

i=0;
for ekey in pdbsf1.keys():
    arow=pdbsf1[ekey];

    v1=arow['s1data'][0:12];
    v2=arow['s1data'][12:24];
    v3=arow['s1data'][24:36];
    v4=arow['s1data'][36:48];
    
    
    pos1=i;
    pos2=i*4;
    
    pid[pos1]=arow['LableNumbe']
    pv[pos2+0,:]=v1;
    pv[pos2+1,:]=v2;
    pv[pos2+2,:]=v3;
    pv[pos2+3,:]=v4;
    
    i=i+1;
    
    if (i%1000==0):
        print(i);
        


'''

'''


xresult=model.predict(pv,batch_size=400);
rxresult=np.argmax(xresult,1)


resultdict=dict();
for ii in range(1075787):
    pos1=ii;
    pos2=ii*4;
    thekey=pid[pos1];
    arow=dict();
    arow['LableNumbe']=thekey;
    arow['d2018']=rxresult[pos2+0];
    arow['d2019']=rxresult[pos2+1];
    arow['d2020']=rxresult[pos2+2];
    arow['d2021']=rxresult[pos2+3];
    resultdict[thekey]=arow;

    if (ii%1000==0):
        print(ii);

np.save('K:\\a-paper2023-gisdata\\adataset\\decision\\mymodel.npy',[resultdict]);    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

    
