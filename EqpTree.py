import wx
from CrtWidget import *
from EqpLibrary import *
import pickle


class EqpTreeFrame(CrtTreeFrame):

    def __init__(self,parent):
        CrtTreeFrame.__init__(self,parent,frametitle='Equipment Setup Panel',
                              rootlabel='[ Equipment List ]',treelist=EqpList,img=("icon1.bmp","icon2.bmp"),spdistance=250,sxy=(770,700),pxy=(150,100))
        self._DoLayout()
        self._Update()
        self.Show()

        
    def _DoLayout(self):
        wx.StaticText(self.panel,-1,'1. Doule-click on the model number to add the equipment for different category.\n\n'+
                                    '2. Select GPIB address for the added-in equipment.\n\n'+
                                    '3. Press on the category button for advanced setup.', pos=(10,10))
        self.panel.SetBackgroundColour(c_silver1) 
        posy=140
        wx.StaticLine(self.panel,-1,(5,posy-35),(500,2),style=wx.LI_HORIZONTAL)
        
        text=wx.StaticText(self.panel,-1,'Select Equipment Model and Assign GPIB Address.', pos=(10,posy-20))    
        font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        text.SetFont(font)
        self.Idch1,self.Idch2,self.Idch3=wx.NewId(),wx.NewId(),wx.NewId()
        self.Idbu1,self.Idbu2,self.Idbu3=wx.NewId(),wx.NewId(),wx.NewId()       #Event binding are put under the method CrtCombo.
            
        sizer=wx.BoxSizer(wx.VERTICAL)
        self.but1,self.tc1,self.ch1,s1=self.CrtCombo('1. Vector Network Analyzer',Idch=self.Idch1,Idbu=self.Idbu1)
        self.but2,self.tc2,self.ch2,s2=self.CrtCombo('2. Spectrum Analyzer',Idch=self.Idch2,Idbu=self.Idbu2)
        self.but3,self.tc3,self.ch3,s3=self.CrtCombo('3. Positioning Controller',Idch=self.Idch3,Idbu=self.Idbu3)

        sizer.Add(s1,0,wx.UP,border=140)
        sizer.Add(s2,0,0,border=0)
        sizer.Add(s3,0,0,border=0)
        self.panel.SetSizer(sizer)
        sizer.Fit(self.panel)
                                                                                                                             
   
        
    def __del__(self):  #When the frame is closed, all the equipment settings are written into eqpsetup.ini.
        setupfile=open('eqpsetup.ini','wb')
        pickle.dump(EqpConfig,setupfile)
        setupfile.close()
        self.parent.Enable(True)
        
    def _Update(self):
        setupfile=open('eqpsetup.ini','rb')
        EqpConfig=pickle.load(setupfile)
        setupfile.close()
                       
        if EqpConfig['vna']['_GPIB'] != None: self.ch1.SetSelection(EqpConfig['vna']['_GPIB'])
        if EqpConfig['spe']['_GPIB'] != None: self.ch2.SetSelection(EqpConfig['spe']['_GPIB'])         
        if EqpConfig['pos']['_GPIB'][0] != None: self.ch3.SetSelection(EqpConfig['pos']['_GPIB'][0])    

        if EqpConfig['vna']['eqpname'] != None: self.tc1.SetValue(EqpConfig['vna']['eqpname'])
        if EqpConfig['spe']['eqpname'] != None: self.tc2.SetValue(EqpConfig['spe']['eqpname'])        
        if EqpConfig['pos']['eqpname'] != None: self.tc3.SetValue(EqpConfig['pos']['eqpname'])
        
    def OnDClick(self,event):
        eqptype=self.tree.GetItemText(event.GetItem())
        try:
            if EqpNumber[eqptype]/100==1:
                self.tc1.SetValue(eqptype)
                EqpConfig['vna']['eqpno']=EqpNumber[eqptype]
                EqpConfig['vna']['eqpname']=eqptype
            elif EqpNumber[eqptype]/100==2:
                self.tc2.SetValue(eqptype)
                EqpConfig['spe']['eqpno']=EqpNumber[eqptype]
                EqpConfig['spe']['eqpname']=eqptype
            elif EqpNumber[eqptype]/100==3:
                self.tc3.SetValue(eqptype)
                EqpConfig['pos']['eqpno']=EqpNumber[eqptype]
                EqpConfig['pos']['eqpname']=eqptype
            else:
                pass
        except:
            pass

    def OnChoice(self,event):
        if event.GetId()==self.Idch1:
            EqpConfig['vna']['_GPIB']=int(self.ch1.GetSelection())
        elif event.GetId()==self.Idch2:
            EqpConfig['spe']['_GPIB']=int(self.ch2.GetSelection())
        elif event.GetId()==self.Idch3:
            EqpConfig['pos']['_GPIB'][0]=int(self.ch3.GetSelection())
        else:
            pass

    def OnButton(self,event):
        if event.GetId()==self.Idbu1:
            self.SetupVna()
        elif event.GetId()==self.Idbu2:
            pass
        elif event.GetId()==self.Idbu3:
            self.SetupPos()
        else:
            pass
                
        
    def CrtCombo(self,caption,Idch,Idbu):
        sxy=(185,30)
        button=wx.Button(self.panel,Idbu,caption,size=(sxy[0]-20,sxy[1]),style=wx.BU_LEFT)
        textctrl=wx.TextCtrl(self.panel,id=-1,value='Insert New Equipment',size=sxy,style=wx.TE_READONLY)
        choice=wx.Choice(self.panel, id=Idch,choices=AddressList)
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(button,0,wx.ALL,border=10)
        sizer.Add(textctrl,0,wx.ALL,border=10)
        sizer.Add(choice,0,wx.ALL,border=13)           
        self.Bind(wx.EVT_CHOICE,self.OnChoice,choice)
        self.Bind(wx.EVT_BUTTON,self.OnButton,button)        
        return button,textctrl,choice,sizer


#Class SetupVna defineds the frame interface for VNA advanced setup.  Class Adv_Vna defines all the handlers from the events triggered within SetupVna frame.
    def SetupVna(self):
        #Instanstiate the frame from CrtWiget.py.
        telf=Adv_Vna(self,frametitle='Advanced Setup: Vector Newtwork Analyzer')
        telf.parent=self
        telf.panel.SetBackgroundColour((230, 255, 222))
        #Defind Layout
        telf.t0,telf.tc0,s0=telf.TextandCtrl('Change Equipment Name:','%s'% EqpConfig['vna']['eqpname'])
        telf.t1,telf.c1,s1,chid1=telf.TextandChoice('IF Bandwidth (Hz):',ChoiceList=IFBList)
        telf.t2,telf.c2,s2,chid1=telf.TextandChoice('Number of port:',ChoiceList=['2','4'])        
        telf.t3,telf.c3,s3,chid3=telf.TextandChoice('Port1 Power Level (dBm):',ChoiceList=PWRList)
        telf.t4,telf.c4,s4,chid4=telf.TextandChoice('Porr2 Power Level (dBm):',ChoiceList=PWRList)        
        sizer = wx.BoxSizer(wx.VERTICAL)
        for s in (s0,s1,s2,s3,s4):
            sizer.Add(s,0,wx.ALL,border=10)
        telf.panel.SetSizer(sizer)
        sizer.Fit(telf.panel)
        #Update the widgets values from EqpConfig list.
        telf.InitUpdate()
        #Binding to pass equipment name into the advanced frame.
        telf.Bind(wx.EVT_TEXT,telf.Update0,telf.tc0)
        #Binding to automatically update the EqpConfig list from the choice boxes. 
        telf.Bind(wx.EVT_CHOICE,telf.Update1,telf.c1)
        telf.Bind(wx.EVT_CHOICE,telf.Update2,telf.c2)      
        telf.Bind(wx.EVT_CHOICE,telf.Update3,telf.c3)
        telf.Bind(wx.EVT_CHOICE,telf.Update3,telf.c4)            
        telf.Show()
        

    
#Class SetupPos defineds the frame interface for VNA advanced setup.  Class Adv_Pos defines all the handlers from the events triggered within SetupPos frame.    
    def SetupPos(self):
        NumberList = ['0','1','2']
        AddressList = [str(x) for x in range(31)]
        AddressList.append('None')
        #Instantiate the frame from CrtWidget.py.
        telf=Adv_Pos(self,frametitle='Advanced Setup: Positioner')
        telf.parent=self
        telf.panel.SetBackgroundColour((230, 255, 222))
        #Do the frame layout.
        telf.t0,telf.c0,s0,chid0=telf.TextandChoice('Number of devices to control?',ChoiceList=NumberList)
        telf.t1,telf.c1,s1,chid1=telf.TextandChoice('GPIB of the 1st positioner (Pos1)',ChoiceList=AddressList)
        telf.t2,telf.c2,s2,chid2=telf.TextandChoice('GPIB of the 2nd positioner (Pos2)',ChoiceList=AddressList)

        sizer = wx.BoxSizer(wx.VERTICAL)
        for s in (s0,s1,s2):
            sizer.Add(s,0,wx.ALL,border=10)
        telf.panel.SetSizer(sizer)
        sizer.Fit(telf.panel)
        #Start the initial updates.
        telf.InitUpdate()       
        #Binding to automatically update the EqpConfig list from the choice boxes. 
        telf.Bind(wx.EVT_CHOICE,telf.Update0,telf.c0)
        telf.Bind(wx.EVT_CHOICE,telf.Update1,telf.c1)      
        telf.Bind(wx.EVT_CHOICE,telf.Update2,telf.c2)        
        telf.Bind(wx.EVT_CLOSE,telf.OnClose)
        
        telf.Show()

class Adv_Pos(CrtFrame):
    def InitUpdate(telf):  #Restore the parameters from EqpConfig list
        if EqpConfig['pos']['nod'] != None: telf.c0.SetSelection(EqpConfig['pos']['nod'])
        if EqpConfig['pos']['_GPIB'][0] != None: telf.c1.SetSelection(EqpConfig['pos']['_GPIB'][0])
        if EqpConfig['pos']['_GPIB'][1] != None: telf.c2.SetSelection(EqpConfig['pos']['_GPIB'][1])
        
    
    def Update0(telf,event):
        EqpConfig['pos']['nod']=telf.c0.GetSelection()
        
    def Update1(telf,event):
        EqpConfig['pos']['_GPIB'][0]=eval(telf.c1.GetStringSelection())
        telf.parent.ch3.SetSelection(EqpConfig['pos']['_GPIB'][0])        

    def Update2(telf,event):
        EqpConfig['pos']['_GPIB'][1]=eval(telf.c2.GetStringSelection())
        
    def OnClose(telf,event):  #Use OnClose method to check the input parameters.
        cnt=lambda a : (not a[0])+(not a[1])+(not a[2])
        n=3-cnt(EqpConfig['pos']['_GPIB'])
 
        if n==0 and EqpConfig['pos']['nod']==None:
            pass
        
        elif n != EqpConfig['pos']['nod']:
            dlg=wx.MessageDialog(telf,"Warning: Number of device does not match the number of GPIB assignments!",style=wx.OK)
            dlg.ShowModal()
        else:
            pass

        if ((EqpConfig['pos']['_GPIB'][0] != None) and (EqpConfig['pos']['_GPIB'][0]==EqpConfig['pos']['_GPIB'][1]) or
            (EqpConfig['pos']['_GPIB'][1] != None) and (EqpConfig['pos']['_GPIB'][1]==EqpConfig['pos']['_GPIB'][2]) ):
            dlg=wx.MessageDialog(telf,"Warning: Duplicate GPIB address!",style=wx.OK)
            dlg.ShowModal()
            flag_close=0
            
        if EqpConfig['pos']['_GPIB'][0]==None and EqpConfig['pos']['_GPIB'][1]!=None:
            dlg=wx.MessageDialog(telf,"Warning: GPIB address needs to be assigned sequentially!",style=wx.OK)
            dlg.ShowModal()
  
        telf.Destroy()

        
class Adv_Vna(CrtFrame):
    def InitUpdate(telf):
        telf.c1.SetStringSelection(str(EqpConfig['vna']['_IFB']))
        telf.c2.SetStringSelection(str(EqpConfig['vna']['_NOP']))        
        telf.c3.SetStringSelection(str(EqpConfig['vna']['_PWR'][0]))
        telf.c4.SetStringSelection(str(EqpConfig['vna']['_PWR'][1]))   
      
    def Update0(telf,event):
        if EqpConfig['vna']['eqpname'] != None:
            EqpConfig['vna']['eqpname']=telf.tc0.GetValue()
            telf.parent.tc1.SetValue(EqpConfig['vna']['eqpname'])
        else:

            dlg=wx.MessageDialog(telf,"Warning: Add equipment from [ Equipment Tree ] first!",style=wx.OK)
            dlg.ShowModal()            

    def Update1(telf,event):
        EqpConfig['vna']['_IFB']=eval(telf.c1.GetStringSelection())

    def Update2(telf,event):
        EqpConfig['vna']['_NOP']=eval(telf.c2.GetStringSelection())        
  
    def Update3(telf,event):
        EqpConfig['vna']['_PWR'][0]=eval(telf.c3.GetStringSelection())

    def Update4(telf,event):
        EqpConfig['vna']['_PWR'][1]=eval(telf.c4.GetStringSelection())
        
