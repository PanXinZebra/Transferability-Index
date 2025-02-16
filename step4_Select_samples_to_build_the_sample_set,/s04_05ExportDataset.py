import psycopg2
import numpy as np;

conn = psycopg2.connect(database = "paper2023", user = "postgres", password = "panxin", host = "192.168.1.111", port = "5432");
print("Opened database successfully");

sql = 'SELECT * FROM myobjects where processed=0;'

cursor = conn.cursor()
cursor.execute(sql)
results = cursor.fetchall()

nums=len(results);

tx=np.zeros((nums,12),dtype='float32');
ty=np.zeros((nums,1),dtype='float32');

#存储2020特例数据
tx22=np.zeros((nums,12),dtype='float32');


for ii in range(nums):
    aresult=results[ii];
    arow=pdbsf1[aresult[0]];
    
    tx[ii,:]=arow['s1data'][36:48];
    ty[ii,0]=aresult[2];
    tx22[ii,:]=arow['s1data'][24:36];


train_x=[];
train_y1=[];
train_y2=[];

for ii in range(17):
    idx=np.where(ty==ii);
    print("%d----%d=="%(ii,len(idx[0])))
    if (ii<=15):
        ax=np.copy(tx[idx[0],:]);
    else:
        #第16类是特例
        ax=np.copy(tx22[idx[0],:]);
        
    ay=np.copy(ty[idx[0],:]);
    
    if (ii!=0):
        if (ii!=16):
            pass;
            ax=ax[0:100,:];
            ay=ay[0:100,:];
    train_x.append(ax);
    train_y1.append(ay);
        
        
train_x=np.concatenate(train_x,0)
train_y1=np.concatenate(train_y1,0)
train_y2=(train_y1>0)*1
    
    
[tx,ty,train_x,train_x,train_y1,train_y2,train_y1,train_y2]


dbdecision2021=[tx,ty,train_x,train_x,train_y1,train_y2,train_y1,train_y2]

np.save(r'K:\a-paper2023-gisdata\adataset\decsiondataset2021',decsiondataset2021,allow_pickle=True);