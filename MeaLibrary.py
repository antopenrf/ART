import pickle
import EqpLibrary

###--- the start of the measurement list ---###

MeaList=[   


(   '1.  Response Sweep',                (('11.  Frequency Spot_Sweep',    ('111.  S-para Spot_Sweep',     '112.  Spectrum Spot_Sweep'                             )),
                                          ('12.  Frequency Range_Sweep',   ('121.  S-para Range_Sweep',    '122.  Spectrum Range_Sweep'                             )))),  

 
(   '2.  Antenna Pattern Measurement',   (('21.  Single Polarization',    ('211.  EIRP Measurement',       '212.  Single 2D Cut',    '213.  Full 3D Pattern'     )),
                                          ('22.  Dual Polarization',      ('221.  EIRP Measurement',       '222.  Single 2D Cut',    '223.  Full 3D Pattern'     )))),
 

(   '3.  Active Device Characterization',(('31.  DC Measurement',         ('311.  Quiescent Point Measurement',   '312.  DC-IV Curve Tracing'                    )),
                                          ('32.  RF Measurement',         ('321.  Two-Port S-Parameter',          '322.  Bias Sweep'                             )),
                                          ('33.  Noise Measurement',      ('331.  Noise Figure Measurement',                                                                 )))),   
]

demo_mea = ( '9.  Demo',                 (('91.  Demo',                 ('911.  Demo',                '912.  Demo: Frequency Sweep'                      )),
                                          ('92.  Demo',                 ('921.  Demo',                '922.  Demo'                                       ))))


## append demo list
MeaList.append(demo_mea)

###--- the end of the measurement list ---###


MeaID={}
def ArrangList():
    m=0
    for each1 in MeaList:
        m=m+1
        n=0
        MeaID[each1[0]]=m
        for each2 in each1[1]:
            n=n+1
            p=0
            MeaID[each2[0]]=m*10+n
            for each3 in each2[1]:
                p=p+1
                if m == 4: m = 9  ## Put demo tests to category 9.
                MeaID[each3]=m*100+n*10+p
                
ArrangList()

#The following MeaConfig dictionary defines all the required informationt to compose the MeaDB (measurement database) object.
#The 'para' key is used to define the default measurement parameters given in the measurement tree panel; 'value' key is used to show the default settings associated with 'para' definition.
#'eqp' key defines the required equipments that will be used in the test.
#The other keys are for parameters which are not set by defaults, but set with different tests.
#(Defaults, which are stored in 'value', are more for the parameters which won't change from test to test.)
#'axes' key stores the dimension of data axes, the 0th key is the stored data format, ant the following ones are the dimension sequence.
MeaConfig={
    '111':{'para':['_Spara'],
           'value':['S21'],
           'axes':['Spara (dB)','Frequency (MHz)'],
           'eqp':['vna'],
           '_Correction':""
           },

    '212':{'para':['_PrimaryPos','_SecondaryPosEnable','_SecondaryPos','_Spara'],
           'value':['Theta','Yes','Phi','S21'],
           'axes':['Spara (dB)','Frequency (MHz)','Pos1'],
           'eqp':['vna','pos'],
           '_PrimaryStep':0.0,
           '_Polarization':'Theta Pol',
           '_SecondaryFixed':0.0,
           '_Correction':""
           },

    '222':{'para':['_PrimaryPos','_SecondaryPosEnable','_SecondaryPos','_PolarizationSequence','_PolarizationSequentialFlag','_Spara'],
           'value':['Theta','Yes','Phi','Theta/Phi','No','S21/S31']},


    '912':{'para':['_PrimaryPos','_SecondaryPosEnable','_SecondaryPos','_Spara'],
           'value':['Theta','Yes','Phi','S21'],
           'axes':['Spara (dB)','Frequency (MHz)','Pos1'],
           'eqp':[],
           '_PrimaryStep':0.0,
           '_Polarization':'Theta Pol',           
           '_SecondaryFixed':0.0,
           '_Correction':""
           }

}


def IniCreate():
    global MeaConfig
    try:
        setupfile=open('measetup.ini','rb')
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
        MeaConfig=temp
        
    setupfile=open('measetup.ini','wb')
    pickle.dump(MeaConfig,setupfile)
    setupfile.close()
    
IniCreate()


PosList=['Theta','Phi']
YNList=['Yes','No']
SParaSiglPolList={2:['S21','S12','S11','S22'],4:['S21','S31','S41','S12','S13','S14','S11','S22','S33','S44']}
SParaDualPolList={2:['S21','S12'],4:['S21/S31','S21/S41','S31/S41','S12/S32','S12/S42','S32/S42','S13/S23','S13/S43','S23/S43','S14/S24','S14/S34','S24/S34']}
PolSeqList=['Theta/Phi','Phi/Theta']


def SetupQuestion():
    return{

    '111':{'questions':['1. Measured S-parameter?'],
           'choices':[SParaSiglPolList[pickle.load(open('eqpsetup.ini','rb'))['vna']['_NOP']]]},
        
    '212':{'questions':['1. Select the primary rotational positioner.','2. Is the secondary positioner enabled?','3. Select the secondary positioner.','4. Measured S-parameter?'],
           'choices':[PosList,YNList,PosList,SParaSiglPolList[pickle.load(open('eqpsetup.ini','rb'))['vna']['_NOP']]]},
    
    '222':{'questions':['1. Select the primary rotational positioner.','2. Is the secondary positioner enabled?','3. Select the secondary positioner.','4. Measured polarization?',
                        '5. Will the polarization be measured sequentially?','6. Measured S-parameter?'],
           'choices':[PosList,YNList,PosList,PolSeqList,YNList,SParaDualPolList[pickle.load(open('eqpsetup.ini','rb'))['vna']['_NOP']]]},

    '912':{'questions':['1. Select the primary rotational positioner.','2. Is the secondary positioner enabled?','3. Select the secondary positioner.','4. Measured S-parameter?'],
           'choices':[PosList,YNList,PosList,SParaSiglPolList[pickle.load(open('eqpsetup.ini','rb'))['vna']['_NOP']]]}
    }

class meadscrp:
### Mark 212 and 222 as _under_contruction first, and focus on 111. 
    content111=("'Measurement 111' does frequency sweep with VNA.")

    
    _under_construction_content212=("'Measurement 212' carries out 2D antenna pattern measurement."+
               "  With one rotational position orbiting the EUT in one direction,"+
               " the 2D patterns of X-Y cut, Y-Z cut or X-Z cut can be measured.")



    _under_construction_content222=("'Measurement 222' carries out 2D antenna pattern measurement.\n")
