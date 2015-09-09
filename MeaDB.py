from MeaLibrary import *
from EqpLibrary import *
import os.path
import pickle

MeaDBList=[]
MeaDBIndex=[]
mea_tagid=0 #tag tracking for total test cases.
 

def DBremove(dbitem):
    MeaDBIndex.remove(MeaDBIndex[MeaDBList.index(dbitem)])
    MeaDBList.remove(dbitem)


def DBadd(dbitem):
    MeaDBList.append(dbitem)
    global mea_tagid
    mea_tagid+=1
    MeaDBIndex.append(mea_tagid)

class MeadbGenerator():
    def __init__(self, meaframe, meatype, meaID, count, name):
        self.meatype=meatype
        self.meaframe=meaframe ## This links to the measurement panel instance (MeaPanel, inherited by CrtMea###).
        self.meaID=meaID
        self.count=count       ## Count in a sequence for each specific meadb.
        self.testinqueue=0     ## Count for current outstanding test items.
        self.meaname=str(mea_tagid+1)+'. '+name
        self.treeID=None
        self.iEqpPara={}
        self.iPara={} ## measurement parameters, associated with the measurement tree setup frame.
        self.iFreq=[] ## frequency list in MHz
        self.flag_in_Testing=0
        self.testname = ''
        self.operatorname = ''
        self.comments = ''
        self.testinglog = ''
        self.UpdatePara()
        self.UpdateEqpPara()
        

    def UpdateFreq(self,flist):
        self._Freq=flist


    def UpdatePara(self):
        """Get the test parameters from measetup.ini, or the defaults from MeaLibrary if measetup.ini doest not exits."""
        filename='measetup.ini'
        if os.path.exists(filename): 
            setupfile=open(filename,'rb')
            temp=pickle.load(setupfile)
            self.iPara[str(self.meaID)]=temp[str(self.meaID)]
            setupfile.close()
        else:
            self.iPara[str(self.meaID)]=MeaConfig[str(self.meaID)]

    def UpdateEqpPara(self):
        filename='eqpsetup.ini'
        if os.path.exists(filename): 
            setupfile=open(filename,'rb')
            self.iEqpPara=pickle.load(setupfile)        
            setupfile.close()
        else:
            self.iEqpPara=EqpConfig
 



        
