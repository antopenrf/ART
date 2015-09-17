import pickle

# the start of the measurement list
EqpList=[   


(   '1. Vector Network Analyzer',         (('Agilent',                 ('E507X ENA',            'N52XX PNA'                                     )),
                                           ('Rohde&Schwarz',           ('ZVL',                'item2'                                         )))),  


(   '2. Spectrum Analyzer',               (('Agilent',                 ('N9020A MXA',           'E4440A PSA'                                    )),
                                           ('Rohde&Schwarz',           ('item3',                'item4'                                         )))),  


(   '8. Rotational Positioner',           (('ETS',                     ('2090',                                                                 )),
                                                                                                                                                  )),  
  
]
# the end of the measurement list

EqpCategory= [ [] for x in range(len(EqpList))]

EqpNumber={'E507X ENA': 111, 'N52XX PNA': 112, 'item2': 122, 'item3': 221, 'ZVL': 121, 'item6': 322, 'item4': 222, 'item5': 321, 'E4440A PSA': 212, '2090': 311, 'N9020A MXA': 211}
EqpIDN={111: 'E507', 112: 'N52XX PNA', 211: 'N9020A MXA', 212: 'E4440A PSA', 311: 'ETS', 121: 'ZVL', 122: 'item2', 221: 'item3', 222: 'item4'}
def ArrangList():
    m=0
    for each1 in EqpList:
        m=m+1   
        n=0
        for each2 in each1[1]:
            n=n+1
            p=0
            for each3 in each2[1]:
                p=p+1
                number = m*100+n*10+p
                EqpCategory[m-1].append(each3)
                EqpNumber[each3]=number
                
ArrangList()

#Here is the dictionary that associates each equipment category with equipment number and _GPIB address.
#The parameters are defined in the nested dictionary.
#equno: equipment number, nod:n number of devices, __GPIB: the address(given in tuple, and the length is given by nod)
#The parameters starting with the underscore _ are for default equipment settings.
EqpConfig={
    'vna':{'eqpno':None,'eqpname':None,'nod':None,'_GPIB':None,'_COM':None,'_IP':None,'_IFB':100,'_PWR':[0,0],'_NOP':2,'_CTRL1':'GPIB'},
    
    'spe':{'eqpno':None,'eqpname':None,'nod':None,'_GPIB':None,'_COM':None,'_IP':None, '_CTRL1':'GPIB'},
    
    'pos':{'eqpno':None,'eqpname':None,'nod':None,'_GPIB':[None,None,None],'_COM':[None,None,None],'_IP':[None,None,None],'_CTRL1':'GPIB','_CTRL2':'GPIB'}
    }



def IniCreate():
    global EqpConfig
    try:
        setupfile=open('eqpsetup.ini','rb')
        flag=1
    except:
        flag=0
        flah=0

    if flag==1:
        try:
            temp=pickle.load(setupfile)
            setupfile.close()
            flah=1
        except:
            flah=0
            
    if flah==1:
        EqpConfig=temp
        
    setupfile=open('eqpsetup.ini','wb')
    pickle.dump(EqpConfig,setupfile)
    setupfile.close()
    
IniCreate()



IFBList=['1','10','30','100','1000','10000']
PWRList=[str(x) for x in range(10,-55,-1)]
AddressList = [str(x) for x in range(31)]  
