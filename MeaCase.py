import wx
import wx.grid  
import MeaPlot
import MeaDB
import wx.lib.masked.numctrl
NumCtrl=wx.lib.masked.numctrl.NumCtrl
from CrtWidget import *
from admin import *
from MeaPanel import *
from EqpLibrary import *
import Test
import os
 
    
## Since CrtMea212 inherites from MeaPanel, self referes to the MeaPanel Frame itself; parent here refers to the Main GUI frame.        
## Rename the CrtMea212 class as '_under_contruction_CrtMea212' to indicate it is not completed yet.
## Focus on CrtMea111 first.

class CrtMea000(MeaPanel):
    def __init__(self, parent, meatype, meaID, name, meadb):  #This parent is the MainGUI frame.
        self.projtree = parent.projtree ## This is the project tree that is going to be passed to MeaPanel.
        self.testlist = parent.testlist ## This is the test queue that is going to be passed to MeaPanel.
        self.imagelist = parent.imagelist
        self.parent = parent

        if self.mode == 'new':
            ###-------------IMPORTANT ... measurement database generated here as "self.meadb" from MeaPanel.GeneMeaDB method ----------###
            self.GeneMeaDB(meatype, meaID, MeaPanel.count, name)
            self.GPIB_token = parent.GPIB_token
            MeaPanel.count += 1
        elif self.mode == 'raw':
            self.meadb = meadb ## This is the meadb that comes from TestDB.meadb.
            self.meadb.meaframe = self
            self.GPIB_token = parent.GPIB_token            
        else:
            pass
        MeaPanel.__init__(self, parent, title = meatype + ' :       ( '+ self.meadb.meaname+' ) ')

    def OnRunBut(self,event):
        self._Run()
        
    def _Run(self):
        ##testnumber = ("Test.test" + self.__class__.__name__[-3:])
        eval("Test.test" + self.__class__.__name__[-3:])(self.meadb)


                

class CrtMea212(CrtMea000): 
    count=0
    def __init__(self, parent, meatype, meaID, name, meadb = None, mode = 'new'):  #This parent is the MainGUI frame.
        CrtMea212.count+=1
        self.mode = mode
        CrtMea000.__init__(self, parent, meatype, meaID, name, meadb)
        
        telf=self.panelW
       
        ####--- The following widgets are specific for CrtMea---------####
        #----Instantialize Frequency Control Widget---#
        telf.sizer_F=self.CrtFreqEntry(telf)

        #----Set up the primary rotation step.--------#
        telf.sizer_Pos=self.CrtOneAxis(telf, self.meadb)
        ####--- The above widgets are specific for CrtMea-------------####
       
        ## Set the sizer for the quick mode by the in-class method (SetSizer)
        self.SetSizer(telf)

        ## Set the axes lables for the plotter
        xdimension=self.meadb.iPara[str(self.meadb.meaID)]['axes'][1]
        ydimension=self.meadb.iPara[str(self.meadb.meaID)]['axes'][0]
        self.plotter.drawlabels(xdimension,ydimension)
        
        ## The following are for advanced mode.
        self.Adv_MeaSetup(telf)
        self.Adv_EqpSetup(telf)
        self.Show()
        
    def SetSizer(self,telf):    
        telf.sizerALL=wx.BoxSizer(wx.VERTICAL)
        telf.sizerALL.Add(telf.RunBut,0,wx.RIGHT,border=580) 
        telf.sizerALL.Add(telf.sizer_F,0,wx.DOWN|wx.UP,border=10)
        telf.sizerALL.Add(telf.sizer_Pos,0,wx.DOWN,border=220)        
        telf.SetSizer(telf.sizerALL)
        telf.sizerALL.Fit(telf)

    def Adv_MeaSetup(self,telf):
        t1, telf.mc1, id1 = self.AdvTextChoice(telf, 'Primary Positioner:', (220,40), ['Theta','Phi'])
        t2, telf.mc2, id2 = self.AdvTextChoice(telf, 'Secondary Positioner:', (220,70), ['Theta','Phi'])        
        t3, telf.mc3, id3 = self.AdvTextChoice(telf, 'Measured Polarization:', (220,100), ['Theta Pol','Phi Pol','None'])
        telf.browser1 = self.CrtCorrectionBrowser1(telf, 'Select the Correction File', (220,140))


        self.AdvMeaIdList=[id1, id2, id3]
        ## This is the list that will be used by the bound method, OnMeaChoic.
        ## In this way, the three same widgets can be bound to the same method.
        for each in [telf.mc1, telf.mc2, telf.mc3]:
            self.Bind(wx.EVT_CHOICE, self.OnMeaChoice, each)
            self.Bind(wx.EVT_TEXT, self.OnBrowser1, telf.browser1)

        self.Update_MeaSetup(telf, self.meadb.meaID, self.meadb.iPara, self.meadb.iEqpPara)
            
    def Update_MeaSetup(self, telf, meaID, iPara, iEqpPara):
        """Retrive default values from the measurement DB."""
        try:
            telf.mc1.SetStringSelection(iPara[str(meaID)]['value'][0])
            telf.mc2.SetStringSelection(iPara[str(meaID)]['value'][2])        
            telf.mc3.SetStringSelection(iPara[str(meaID)]['_Polarization'])
        except KeyError:
            pass


    def Adv_EqpSetup(self,telf):     
        eqt1,telf.eqc1,eqid1=self.AdvTextChoice(telf,'-VNA-',(220,340),EqpCategory[0])
        telf.text_address_vna = wx.StaticText(telf, -1, 'VNA Address:     ', pos=(220, 340+30), style=wx.TE_LEFT)
#        eqt10, telf.eqc10, eqid10=self.AdvTextChoice(telf,'Address:  ',(220,340+30),AddressList)
        t4,telf.mc4,id4=self.AdvTextChoice(telf,'VNA IF Bandwidth (Hz):',(220,340+30*2),IFBList)
        t5,telf.mc5,id5=self.AdvTextChoice(telf,'VNA Input Power (dBm):',(220,340+30*3),PWRList)

        eqt2,telf.eqc2,eqid2=self.AdvTextChoice(telf,'-Rotational Positioner-',(220,340+30*5),EqpCategory[2])
        telf.text_address_pos1 = wx.StaticText(telf, -1, '1st Positioner Address:     ', pos=(220, 340+30*6), style=wx.TE_LEFT)
        telf.text_address_pos2 = wx.StaticText(telf, -1, '2nd Positioner Address:     ', pos=(220, 340+30*7), style=wx.TE_LEFT)
#        eqt20,telf.eqc20,eqid20=self.AdvTextChoice(telf,'1st Positioner GPIB:',(220,340+30*6),AddressList)
#        eqt21,telf.eqc21,eqid21=self.AdvTextChoice(telf,'2nd Positioner GPIB:',(220,340+30*7),AddressList)

        self.AdvEqpIdList=[]        
        for each in [id4, id5, eqid1, eqid2]:
            self.AdvEqpIdList.append(each)
        for each in [telf.mc4, telf.mc5, telf.eqc1, telf.eqc2]:
            self.Bind(wx.EVT_CHOICE,self.OnEqpChoice,each)        

        self.Update_EqpSetup(telf, self.meadb.meaID, self.meadb.iPara, self.meadb.iEqpPara)
        

    def Update_EqpSetup(self, telf, meaID, iPara, iEqpPara):
        """Retrive equipment values from the measurement DB."""
        if iPara[str(meaID)]['value'][1]=='No': telf.eqc21.Disable()
        
        try:
            telf.eqc1.SetStringSelection(revdict(EqpNumber)[iEqpPara['vna']['eqpno']])
            telf.eqc1.Disable()
            telf.text_address_vna.SetLabel('VNA Address:       ' + iEqpPara['vna']['_'+iEqpPara['vna']['_CTRL1']])
#            telf.eqc10.SetStringSelection(str(iEqpPara['vna']['_'+iEqpPara['vna']['_CTRL1']]))
#            telf.eqc10.Disable()
            telf.mc4.SetStringSelection(str(iEqpPara['vna']['_IFB']))
            telf.mc5.SetStringSelection(str(iEqpPara['vna']['_PWR'][0]))
        except KeyError:
            pass        

        try:        
            telf.eqc2.SetStringSelection(revdict(EqpNumber)[iEqpPara['pos']['eqpno']])
            telf.eqc2.Disable()
            telf.text_address_pos1.SetLabel('1st Positioner Address:       ' + iEqpPara['pos']['_'+iEqpPara['pos']['_CTRL1']][0])
            telf.text_address_pos2.SetLabel('2nd Positioner Address:      ' + iEqpPara['pos']['_'+iEqpPara['pos']['_CTRL2']][1])  ## needs to revisit
            #            telf.eqc20.SetStringSelection(str(iEqpPara['pos']['_GPIB'][0]))
#            telf.eqc21.SetStringSelection(str(iEqpPara['pos']['_GPIB'][1]))
        except KeyError:
            pass
        

    def OnMeaChoice(self,event):
        selected=event.GetId()
        selectedChoice=self.panelW.FindWindowById(selected).GetStringSelection()
        def Update(selectedID):           
            for each in self.AdvMeaIdList:
                if each == selectedID:
                    if self.panelW.FindWindowById(selectedID)==self.panelW.mc1:
                        self.meadb.iPara[str(self.meadb.meaID)]['value'][0]=self.panelW.FindWindowById(selectedID).GetStringSelection()
                    if self.panelW.FindWindowById(selectedID)==self.panelW.mc2:
                        self.meadb.iPara[str(self.meadb.meaID)]['value'][2]=self.panelW.FindWindowById(selectedID).GetStringSelection()
                    if self.panelW.FindWindowById(selectedID)==self.panelW.mc3:
                        self.meadb.iPara[str(self.meadb.meaID)]['_Polarization']=self.panelW.FindWindowById(selectedID).GetStringSelection()

        if selectedChoice == 'Theta' or selectedChoice == 'Phi':
            anotherid=ChoiceExclusion(self.panelW,selected,[self.AdvMeaIdList[0],self.AdvMeaIdList[1]],['Theta','Phi'])
            Update(anotherid)
        Update(selected)

    def OnBrowser1(self,event):
        telf=self.panelW
        self.meadb.iPara[str(self.meadb.meaID)]['_Correction']=telf.browser1.GetValue()
    
    def OnEqpChoice(self,event):
        selectedID=event.GetId()
        selectedChoice=self.panelW.FindWindowById(selectedID).GetStringSelection()
        for each in self.AdvEqpIdList:
            if each == selectedID:
                if self.panelW.FindWindowById(selectedID)==self.panelW.eqc1:
                    self.meadb.iEqpPara['vna']['eqpno']=EqpNumber[self.panelW.FindWindowById(selectedID).GetStringSelection()]
                    self.meadb.iEqpPara['vna']['eqpname']=revdict(EqpNumber)[self.meadb.iEqpPara['vna']['eqpno']]                   
                if self.panelW.FindWindowById(selectedID)==self.panelW.eqc2:
                    self.meadb.iEqpPara['pos']['eqpno']=EqpNumber[self.panelW.FindWindowById(selectedID).GetStringSelection()]
                    self.meadb.iEqpPara['pos']['eqpname']=revdict(EqpNumber)[self.meadb.iEqpPara['pos']['eqpno']]                        
                if self.panelW.FindWindowById(selectedID)==self.panelW.eqc10:
                    self.meadb.iEqpPara['vna']['_GPIB']=int(self.panelW.FindWindowById(selectedID).GetStringSelection())
                if self.panelW.FindWindowById(selectedID)==self.panelW.eqc20:
                    self.meadb.iEqpPara['pos']['_GPIB'][0]=int(self.panelW.FindWindowById(selectedID).GetStringSelection())
                if self.panelW.FindWindowById(selectedID)==self.panelW.eqc21:
                    self.meadb.iEqpPara['pos']['_GPIB'][1]=int(self.panelW.FindWindowById(selectedID).GetStringSelection())                       
                if self.panelW.FindWindowById(selectedID)==self.panelW.mc4:                    
                    self.meadb.iEqpPara['vna']['_IFB']=self.panelW.FindWindowById(selectedID).GetStringSelection()
                if self.panelW.FindWindowById(selectedID)==self.panelW.mc5:                    
                    self.meadb.iEqpPara['vna']['_PWR'][0]=int(self.panelW.FindWindowById(selectedID).GetStringSelection())



 


### Mea 111 - frequency sweep over VNA
class CrtMea111(CrtMea000):
    count=0
    def __init__(self, parent, meatype, meaID, name, meadb = None, mode = 'new'):  #This parent is the MainGUI frame.
        CrtMea111.count+=1
        self.mode = mode
        CrtMea000.__init__(self, parent, meatype, meaID, name, meadb)

        telf=self.panelW

        ####----The following widgets are specific for CrtMea---------####
        #----Instantialize Frequency Control Widget---#
        telf.sizer_F=self.CrtFreqEntry(telf)

        #Set the sizer for the quick mode by the in-class method (SetSizer)
        self.SetSizer(telf)

        #Set the axes lables for the plotter
        xdimension=self.meadb.iPara[str(self.meadb.meaID)]['axes'][1]
        ydimension=self.meadb.iPara[str(self.meadb.meaID)]['axes'][0]
        self.plotter.drawlabels(xdimension,ydimension)
        
        #The following are for advanced mode.
        self.Adv_MeaSetup(telf)
        self.Adv_EqpSetup(telf)        
        self.Show()


    def SetSizer(self,telf):    
        text_dummy = wx.StaticText(self.panelW, -1, pos=(10,300), size=(100,450), label='')
        ## This is dummy StaticText to extend the available cavas size.
        telf.sizerALL=wx.BoxSizer(wx.VERTICAL)
        telf.sizerALL.Add(telf.RunBut,0,wx.RIGHT,border=580) 
        telf.sizerALL.Add(telf.sizer_F,0,wx.DOWN|wx.UP,border=10)
        telf.sizerALL.Add(text_dummy, 0)  ## Add the dummy text.
        telf.SetSizer(telf.sizerALL)
        telf.sizerALL.Fit(telf)


    def Adv_MeaSetup(self,telf):
        t1, telf.mc1, id1 = self.AdvTextChoice(telf, 'S Parameter:',(220,40),['S21','S11', 'S12', 'S22'])
        telf.browser1=self.CrtCorrectionBrowser1(telf, 'Select the Correction File', (220,70))
        self.Bind(wx.EVT_CHOICE, self.OnMeaChoice, telf.mc1)
        self.Bind(wx.EVT_TEXT, self.OnBrowser1, telf.browser1)
        self.Update_MeaSetup(telf, self.meadb.meaID, self.meadb.iPara, self.meadb.iEqpPara)
        
    def Update_MeaSetup(self, telf, meaID, iPara, iEqpPara):
        telf.mc1.SetStringSelection(iPara[str(meaID)]['value'][0])
        

    def Adv_EqpSetup(self,telf):      
        eqt1, telf.eqc1, eqid1 = self.AdvTextChoice(telf,'-VNA-',(220,340),EqpCategory[0])
        telf.text_address = wx.StaticText(telf, -1, 'VNA Address:     ', pos=(220, 340+30), style=wx.TE_LEFT)
        t4,telf.mc4,id4=self.AdvTextChoice(telf,'VNA IF Bandwidth (Hz):',(220,340+30*2),IFBList)
        t5,telf.mc5,id5=self.AdvTextChoice(telf,'VNA Input Power (dBm):',(220,340+30*3),PWRList)

        self.AdvEqpIdList=[]        
        for each in [id4, id5, eqid1]:
            self.AdvEqpIdList.append(each)
        for each in [telf.mc4, telf.mc5, telf.eqc1]:
            self.Bind(wx.EVT_CHOICE, self.OnEqpChoice,each)        

        self.Update_EqpSetup(telf, self.meadb.meaID, self.meadb.iPara, self.meadb.iEqpPara)

        
    def Update_EqpSetup(self, telf, meaID, iPara, iEqpPara):
        try:            
            telf.eqc1.SetStringSelection(revdict(EqpNumber)[iEqpPara['vna']['eqpno']])
            telf.eqc1.Disable()
            telf.text_address.SetLabel('VNA Address:       ' + iEqpPara['vna']['_'+iEqpPara['vna']['_CTRL1']])
            telf.mc4.SetStringSelection(str(iEqpPara['vna']['_IFB']))
            telf.mc5.SetStringSelection(str(iEqpPara['vna']['_PWR'][0]))
        except KeyError:
            pass        

    def OnMeaChoice(self, event):
        telf = self.panelW
        self.meadb.iPara[str(self.meadb.meaID)]['value'][0] = telf.mc1.GetStringSelection()
            
    def OnBrowser1(self,event):
        telf=self.panelW
        self.meadb.iPara[str(self.meadb.meaID)]['_Correction']=telf.browser1.GetValue()

    
    def OnEqpChoice(self,event):
        selectedID=event.GetId()
        selectedChoice=self.panelW.FindWindowById(selectedID).GetStringSelection()
        for each in self.AdvEqpIdList:
            if each == selectedID:
#                if self.panelW.FindWindowById(selectedID)==self.panelW.eqc1:
#                    self.meadb.iEqpPara['vna']['eqpno']=EqpNumber[self.panelW.FindWindowById(selectedID).GetStringSelection()]
#                    self.meadb.iEqpPara['vna']['eqpname']=revdict(EqpNumber)[self.meadb.iEqpPara['vna']['eqpno']]                                          
#                if self.panelW.FindWindowById(selectedID)==self.panelW.eqc10:
#                    self.meadb.iEqpPara['vna']['_GPIB']=int(self.panelW.FindWindowById(selectedID).GetStringSelection())
                if self.panelW.FindWindowById(selectedID)==self.panelW.mc4:                    
                    self.meadb.iEqpPara['vna']['_IFB']=self.panelW.FindWindowById(selectedID).GetStringSelection()
                if self.panelW.FindWindowById(selectedID)==self.panelW.mc5:                    
                    self.meadb.iEqpPara['vna']['_PWR'][0]=int(self.panelW.FindWindowById(selectedID).GetStringSelection())

#    def OnRunBut(self,event):
#        test111(self.meadb)

class CrtMea912(CrtMea111):
    """Demo only"""


 






