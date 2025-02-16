'''
生成framedb文件， 这个文件带外框，所以会降低比对次数
'''

plist=[]

for key in pdb.keys():
    value=pdb[key]['PageNumber'];
    plist.append(value);
npplist=np.array(plist)
pnumber=np.unique(npplist);


framedb=dict();

for pagepos in pnumber:    
    xmin=99999999999;
    xmax=-9999999999;
    ymin=99999999999;
    ymax=-9999999999;
    print(pagepos);
    keylist=[];
    for key in pdb.keys():
        value=pdb[key]['PageNumber'];
        if (value!=pagepos):
            continue;
        px=pdb[key]['PX'];
        py=pdb[key]['PY'];
        keylist.append(key);
        if (xmin>px):
            xmin=px;
        if (xmax<px):
            xmax=px;
        if (ymin>py):
            ymin=py;
        if (ymax<py):
            ymax=py;
    border=[xmin,xmax,ymin,ymax];
    framedb[pagepos]=[border,keylist];

np.save(framefile,[framedb]);
    