# -*- coding: utf-8 -*-
"""
Created on Thu May 12 16:14:20 2016

@author: salem7mg
"""
import multiprocessing as mp
import talib
import math
from MyAi import MyAi
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


from MyInd import MyInd
import numpy as np
import math 
import os

# n_estimators,min_samples_split,max_depth
Ind=[[0,'CAN','CAN',  (0,),[0],[50,10,3]],
     [0,'BBANDS212','BBANDS',(3,),  [21,2.0,2.0,0],[5,5,3]],
     [0,'BBANDS213','BBANDS',(3,),  [21,3.0,3.0,0],[20,5,3]],
     [0,'BBANDS842','BBANDS',(3,),  [84,2.0,2.0,0],[5,5,3]],
     [0,'BBANDS843','BBANDS',(3,),  [84,3.0,3.0,0],[20,5,3]],
     [0,'Ich','Ich',  (),[],[20,5,3]],
     [1,'MACD8_17_9','MACD',  (3,),[8,17,9],[10,5,3]],
     [1,'MACD12_26_9','MACD',  (3,),[12,26,9],[30,5,5]],
     [1,'ADX9','ADX', (1,2,3), [9],[5,5,3]],
     [1,'ADX21','ADX', (1,2,3), [21],[300,5,3]],
     [1,'ADXR12','ADX', (1,2,3), [12],[5,5,3]],
     [1,'ADXR26','ADX', (1,2,3), [26],[5,15,3]],
#     [1,'ATR9','ATR',  (1,2,3),[9],[5,15,3]],
#     [1,'ATR30','ATR',  (1,2,3),[30],[5,15,3]],
#     [2,'CANV','CANV',  (0,),[0],[50,5,10]],
     [0,'MA9','MA',  (3,),[9],[300,15,3]],
     [0,'MA17','MA',  (3,),[17],[5,5,3]],
     [0,'MA26','MA',  (3,),[26],[20,5,3]],
     [0,'MA33','MA',  (3,),[33],[20,10,3]],
     [0,'MA42','MA',  (3,),[42],[20,10,3]],
     [0,'MA65','MA',  (3,),[65],[30,5,3]],
     [0,'MA76','MA',  (3,),[76],[5,15,3]],
     [0,'MA129','MA',  (3,),[129],[5,5,3]],
     [0,'MA172','MA',  (3,),[172],[5,5,3]],
     [0,'MA200','MA',  (3,),[200],[100,5,3]],
     [0,'SMA9','SMA',  (3,),[9],[300,15,3]],
     [0,'SMA17','SMA',  (3,),[17],[5,5,3]],
     [0,'SMA26','SMA',  (3,),[26],[20,5,3]],
     [0,'SMA33','SMA',  (3,),[33],[20,10,3]],
     [0,'SMA42','SMA',  (3,),[42],[20,10,3]],
     [0,'SMA65','SMA',  (3,),[65],[30,5,3]],
     [0,'SMA76','SMA',  (3,),[76],[5,15,3]],
     [0,'SMA129','SMA',  (3,),[129],[5,5,3]],
     [0,'SMA172','SMA',  (3,),[172],[5,5,3]],
     [0,'SMA200','SMA',  (3,),[200],[100,5,3]],
     [0,'EMA9','EMA',  (3,),[9],[300,15,3]],
     [0,'EMA17','EMA',  (3,),[17],[5,5,3]],
     [0,'EMA26','EMA',  (3,),[26],[10,5,3]],
     [0,'EMA33','EMA',  (3,),[33],[20,10,3]],
     [0,'EMA42','EMA',  (3,),[42],[20,10,3]],
     [0,'EMA65','EMA',  (3,),[65],[5,10,3]],
     [0,'EMA76','EMA',  (3,),[76],[100,15,3]],
     [0,'EMA129','EMA',  (3,),[129],[20,10,3]],
     [0,'EMA172','EMA',  (3,),[172],[30,5,3]],
     [0,'EMA200','EMA',  (3,),[200],[20,10,3]]]

TimeFrame=[5,15,30,60,240,1440,10080,43200]
    
t_cur=["EUR","GBP","AUD","NZD","USD","CAD","CHF","JPY"]


def func_call(s, method,b,l,args = []):
        
    if len(l) ==5 :
        c=b[:,l[0]]
        d=b[:,l[1]]
        e=b[:,l[2]]
        f=b[:,l[3]]
        g=b[:,l[4]]
        out=getattr(s, method)(c,d,e,f,g,*args)
    if len(l) ==4 :
        c=b[:,l[0]]
        d=b[:,l[1]]
        e=b[:,l[2]]
        f=b[:,l[3]]
        out=getattr(s, method)(c,d,e,f,*args)
    if len(l) ==3 :
        c=b[:,l[0]]
        d=b[:,l[1]]
        e=b[:,l[2]]
        out=getattr(s, method)(c,d,e,*args)
    if len(l) ==2 :
        c=b[:,l[0]]
        d=b[:,l[1]]
        out=getattr(s, method)(c,d,*args)
    if len(l) ==1:
        c=b[:,l[0]]
        out=getattr(s, method)(c,*args)
    if len(l) ==0:
        out=MyInd.Ich(b)

    return out

def Indstruct(a,i,j,base):

    if i==j:
        a=[[base[i][0]]]
        return Indstruct(a,i,j+1,base)
    else:
        if j==len(base):
            return a
    x=a[j-i-1][0:]
    x.append(base[j][0])
    a.append(x)
    return Indstruct(a,i,j+1,base)

def IndPredict(can,pre,fit):
    """
    [IndCalc]
    学習用ラベル算出
    """

    l=np.zeros(len(can)-pre-fit) 
    j=0
    k=0
    for c in range(pre,len(l)):
            cmaxi=np.argmax(can[c+1:c+fit+1,3])
            cmini=np.argmin(can[c+1:c+fit+1,3])
            l[c]=0
            if  can[c+1,3]>can[c,3] and can[cmaxi+c,3]>can[c,3]  \
                and  can[cmaxi+c,3]-can[c,3]>can[c,3]-can[cmini+c,3]: 
                #if  (can[cmaxi+c,3]-can[c,3]) > 0.1 and can[c,3]<can[c+1,3]  :               
                l[c-pre]=cmaxi+1
                j=j+1
            elif can[c+1,3]<can[c,3] and can[cmini+c,3]<can[c,3] \
                and can[c,3]-can[cmini+c,3]>can[cmaxi+c,3]-can[c,3]:
                #if  (can[c,3]-can[cmini+c,3]) > 0.1 and can[c,3]>can[c+1,3]:               
                l[c-pre]=cmini*-1-1
                k=k+1
            else:    
                l[c-pre]=0
    return(l)    

def IndCalc(indnamex,can):
    """
    [IndCalc]
    指標値計算
    """

    if indnamex[2]=='CAN':
        IndValue=np.array(can[:,0:4])
    elif indnamex[2]=='CANV':
        IndValue=np.array(can[:,4:5])
    else:    
        s=talib
        IndValue=np.array(func_call(s,indnamex[2],can[:,],indnamex[3],indnamex[4])).reshape(len(can),-1)
        
    return IndValue      

def npJoin(*arg_t):
    """
    [npJoin]
    指標値の結合
    """

    x=np.array(arg_t[0])
    for j in range(1,len(arg_t)):
        x=np.concatenate([x[:],arg_t[j][:]],axis=1)
    return x

def IndRatio(Dayvalue):

    """
    [IndRatio]
    各指標値を正則化
    """
    col = Dayvalue.shape[1]
    # 属性ごとに平均値と標準偏差を計算
    # 属性ごとにデータを標準化
    XX=np.array(Dayvalue)    
    for i in range(len(Dayvalue)):
        mu = np.mean(Dayvalue[i])
        sigma = np.std(Dayvalue[i])
        XX[i] = (Dayvalue[i] - mu) / sigma
    return XX

def argwrapper(args):
    '''
    ラッパー関数
    '''
    return args[0](*args[1:])
    
def IndAi0(Sybol,TimeFrame,aiarg):
    """
    [IndAi0]
    各指標値の取り出し
    """
    filedir='/home/salem7mg/Documents/Python/data/'+Sybol+TimeFrame+"/"
    filedir1='/tmp/'
    filedir2='/tmp/'
    if (len(aiarg)==1):    
        print(Sybol+TimeFrame+Ind[aiarg[0]][1]+"  AI start")
        train=np.load(filedir1+Sybol+TimeFrame+Ind[aiarg[0]][1]+'.npy')
        train=np.array(IndRatio(train))
    if (len(aiarg)==2):
        print(Sybol+TimeFrame+Ind[aiarg[0]][1]+Ind[aiarg[1]][1]+"  AI start")
        train=np.load(filedir2+Sybol+TimeFrame+Ind[aiarg[0]][1]+Ind[aiarg[1]][1]+'.npy')
        os.remove(filedir2+Sybol+TimeFrame+Ind[aiarg[0]][1]+Ind[aiarg[1]][1]+'.npy')
    return train
     
def IndAiPredict(clf,Sybol,TimeFrame,aiarg):

    train=IndAi0(Sybol,TimeFrame,aiarg)
    return clf.predict(train[-1])    

def IndAi(Sybol,TimeFrame,aiarg):
    """
    [IndAi]
    ラベル＋各指標値を使いランダムフォレストによる機械学習
    """
    train=IndAi0(Sybol,TimeFrame,aiarg)    
    #train[np.isnan(train)]=0
    #if len(train)==1:
    filedir='/home/salem7mg/Documents/Python/data/'+Sybol+TimeFrame+"/"
    filedir2='/tmp/'
    nm=filedir+Sybol+TimeFrame+Ind[aiarg[0]][1]
    if (len(aiarg)==2):
        nm=nm+Ind[aiarg[1]][1]
    label=np.load(filedir2+'label'+Sybol+TimeFrame+'.npy')
    train=npJoin(train.reshape(len(train),-1),label.reshape(len(label),1))
    train=train[~np.isnan(train).any(axis=1)]
    
    clf=RandomForestClassifier()
    clf.fit(train[:,:-1],train[:,-1])    
    dmp=joblib.dump(clf,nm)
    del train    
    del label    
    del dmp    
    del clf    
    return
    
def TrVal1(Sybol,TimeFrame,i,can,pre,fit):
    """
    [TrVal1]
    一つ目の指標値を作業用ディレクトリーへ書き込み
    """
    trname=Sybol+str(TimeFrame)+Ind[i][1]
    filedir='/tmp/'
    trval11=np.array(IndCalc(Ind[i],can))
    x=[trval11[j-pre:j].reshape(len(trval11[j-pre:j]),-1)
        for j in range(pre,len(trval11)-fit)] 
    y=np.array(x).reshape(len(x),-1)
    np.save(filedir+trname+'.npy',y)
    del trval11
    del x
    return

def TrValx(Sybol,TimeFrame,i,j):
    """
    [TrValx]
	２種類の指標値を作業用ディレクトリーへ書き込み
    """

    filedir='/tmp/'
    filedir2='/tmp/'
    trvalx1=np.load(filedir+Sybol+TimeFrame+Ind[i][1]+'.npy')
    trvalx2=np.load(filedir+Sybol+TimeFrame+Ind[j][1]+'.npy')
    if Ind[i][0] == 0 and Ind[j][0] == 0:
        trvalxx=IndRatio(npJoin(trvalx1,trvalx2))
        #trvalxx=npJoin(trvalx1,trvalx2)
    elif Ind[i][0] == 0 and Ind[j][0] != 0:
        trvalxx=npJoin(IndRatio(trvalx1),IndRatio(trvalx2))
        #trvalxx=npJoin(trvalx1,trvalx2)
    elif Ind[i][0] !=0 and Ind[j][0] == 0:
        trvalxx=npJoin(IndRatio(trvalx1),IndRatio(trvalx2))
        #trvalxx=npJoin(trvalx1,trvalx2)
    elif Ind[i][0] !=0  and Ind[j][0] !=0 :
        trvalxx=IndRatio(npJoin(trvalx1,trvalx2))
    np.save(filedir2+Sybol+TimeFrame+Ind[i][1]+Ind[j][1]+'.npy',np.array(trvalxx))
    del trvalx1
    del trvalx2
    print(Ind[i][1]+Ind[j][1],"end  ")
    return trvalxx

def IndMain2(Sybol,TimeFrame,fromx,to):
    indx={}
    filedir2='/tmp/'
    filedir='/home/salem7mg/Documents/Python/data'
    #作業用ディレクトリー作成
    if not os.path.exists(filedir):
        os.mkdir(filedir)
        filedir=filedir+'/'+Sybol+TimeRange[j]    
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    #MySQLよりローソク値取得
    can=np.array(MyInd.CanRead(Sybol,TimeFrame,fromx,to))
    #ラベル算出
    label=IndPredict(can,52,3)
    np.save(filedir2+'label'+Sybol+TimeFrame+'.npy',label)
    #一つ目の指標算出
    processes = []
    for i in range(len(Ind)):
        processes.append((TrVal1,Sybol,TimeFrame,i,can,52,3))
    p = mp.Pool(mp.cpu_count())
    p.map(argwrapper,processes)
    p.close()
    del can
    del p 
    processes = []

    #一つ目の機械学習シリアライズ
    for i in range(len(Ind)):            
        aiarg=[]
        aiarg.append(i)
        processes.append((IndAi,Sybol,TimeFrame,aiarg))
    p = mp.Pool(mp.cpu_count())
    p.map(argwrapper,processes)
    p.close()
    del p

    #２つ機械学習シリアライズ

    processes = []
    for i in range(1):
        processes = []
        for j in range(i+1,len(Ind)):
            processes.append((TrValx,Sybol,TimeFrame,i,j))
        p = mp.Pool(mp.cpu_count())
        p.map(argwrapper,processes)
        p.close()
        del p
        processes = []
        for j in range(i+1,len(Ind)):
            aiarg=[]
            aiarg.append(i)
            aiarg.append(j)
            if aiarg[0]>aiarg[1]:
                print("error=",aiarg)
                #return
            processes.append((IndAi,Sybol,TimeFrame,aiarg))
        p = mp.Pool(mp.cpu_count())
        p.map(argwrapper,processes)
        p.close()
        del p
    #作業用ファイル削除
    for i in range(len(Ind)):            
        os.remove(filedir2+Sybol+TimeFrame+Ind[i][1]+'.npy')
    print("end")    
    print (label)
    os.remove(filedir2+'label'+Sybol+TimeFrame+'.npy')
    return(label)

def QueReadx():
    Que=MyInd.QueRead()
    print(Que)
    return

if __name__ == '__main__':
    label=IndMain2('USDJPY','15','0','1167429600')
