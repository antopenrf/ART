import wx
from CrtWidget import *
from EqpLibrary import *
import pickle


class EqpTreeFrame(CrtTreeFrame):

    def __init__(self,parent):
        CrtTreeFrame.__init__(self,parent,frametitle='Equipment Setup Panel',
                              rootlabel='[ Equipment List ]',treelist=EqpList,img=("icon1.bmp","icon2.bmp"),spdistance=250,sxy=(920,700),pxy=(150,100))
        self._DoLayout()
        self._Update()
        self.Show()

        
    def _DoLayout(self):
        wx.StaticText(self.panel,-1,'1. Doule-click on the model number to add the equipment for different category.\n\n'+
                                    '2. Select communication address for the added-in equipment.\n\n'+
                                    '3. Press on the category button for advanced setup.', pos=(10,10))
        self.panel.SetBackgroundColour(c_silver1) 
        posy=140
        wx.StaticLine(self.panel,-1,(5,posy-35),(500,2),style=wx.LI_HORIZONTAL)
        
        text=wx.StaticText(self.panel,-1,'Select Equipment Model and Assign Communication Address.', pos=(10,posy-20))    
        font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        text.SetFont(font)


        def new_Idch():
            return wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId()
        
        #Event binding are put under the method _CrtCombo.
        ## ch1, ch2 and ch3 contains 7 returned wx.choice widgets, 1 gpib, 1 com and 5 for ip (4 numbers plus one port).

        self.equipment_sizer=wx.BoxSizer(wx.VERTICAL)
        self.but1, self.tc1, self.ch1, s1 = self._CrtCombo('1. Vector Network Analyzer',Idch=new_Idch(), Idbu=wx.NewId())
        self.but2, self.tc2, self.ch2, s2 = self._CrtCombo('2. Spectrum Analyzer', Idch=new_Idch(), Idbu=wx.NewId())
        self.but3, self.tc3, self.ch3, s3 = self._CrtCombo('3. Positioning Controller', Idch=new_Idch(), Idbu=wx.NewId())

        self.equipment_sizer.Add(s1,0,wx.UP,border=140)
        self.equipment_sizer.Add(s2,0,wx.UP,border=10)
        self.equipment_sizer.Add(s3,0,wx.UP,border=10)
        self.panel.SetSizer(self.equipment_sizer)
        self.equipment_sizer.Fit(self.panel)  
   
        
    def __del__(self):  #When the frame is closed, all the equipment settings are written into eqpsetup.ini.
        setupfile=open('eqpsetup.ini','wb')
        pickle.dump(EqpConfig,setupfile)
        setupfile.close()
        self.parent.Enable(True)
        
    def _Update(self):
        setupfile=open('eqpsetup.ini','rb')
        EqpConfig=pickle.load(setupfile)
        setupfile.close()
        for each in ['vna', 'spe', 'pos']:
            self.selected_ctrl = each
            if EqpConfig[each]['_CTRL1'] == 'GPIB':
                self._Change_GPIB_Form(mode = 'gpib')
            elif EqpConfig[each]['_CTRL1'] == 'COM':
                self._Change_GPIB_Form(mode = 'com')
            elif EqpConfig[each]['_CTRL1'] == 'IP':
                self._Change_GPIB_Form(mode = 'ip')
            
        if EqpConfig['vna']['_GPIB'] != None: self.ch1[0].SetSelection(EqpConfig['vna']['_GPIB'])
        if EqpConfig['vna']['_COM'] != None: self.ch1[1].SetSelection(EqpConfig['vna']['_COM'])
        if EqpConfig['vna']['_IP'] != None:
            ip_address, port_number = EqpConfig['vna']['_IP'].split(" ")
            ip_address = ip_address.split(".")
            self.ch1[6].SetSelection(int(port_number))            
            for each in (2,3,4,5):
                self.ch1[each].SetSelection(int(ip_address[each-2]))
                                            
        if EqpConfig['spe']['_GPIB'] != None: self.ch2[0].SetSelection(EqpConfig['spe']['_GPIB'])
        if EqpConfig['spe']['_COM'] != None: self.ch2[1].SetSelection(EqpConfig['spe']['_COM'])
        if EqpConfig['spe']['_IP'] != None:        
            ip_address, port_number = EqpConfig['vna']['_IP'].split(" ")
            ip_address = ip_address.split(".")
            self.ch2[6].SetSelection(int(port_number))            
            for each in (2,3,4,5):
                self.ch2[each].SetSelection(int(ip_address[each-2]))
                                            
        if EqpConfig['pos']['_GPIB'][0] != None: self.ch3[0].SetSelection(EqpConfig['pos']['_GPIB'][0])
        if EqpConfig['pos']['_COM'][0] != None: self.ch3[1].SetSelection(EqpConfig['pos']['_COM'][0])
        if EqpConfig['pos']['_IP'][0] != None:
            ip_address, port_number = EqpConfig['pos']['_IP'][0].split(" ")
            ip_address = ip_address.split(".")
            self.ch3[6].SetSelection(int(port_number))                        
            for each in (2,3,4,5):
                self.ch3[each].SetSelection(int(ip_address[each-2]))
        
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

    def _OnChoice(self, event_id, eqp, ch):
        ## eqp: equipment, ch: choice
        if event_id == ch[0].GetId():
            if eqp == 'pos':
                EqpConfig[eqp]['_GPIB'][0] = int(ch[0].GetSelection())
                EqpConfig[eqp]['_COM'][0] = None
                EqpConfig[eqp]['_IP'][0] = None
            else:
                EqpConfig[eqp]['_GPIB'] = int(ch[0].GetSelection())
                EqpConfig[eqp]['_COM'] = None
                EqpConfig[eqp]['_IP'] = None
            for each in (1,2,3,4,5,6):
                ch[each].SetSelection(-1)

        elif event_id == ch[1].GetId():
            if eqp == 'pos':
                EqpConfig[eqp]['_COM'][0] = int(ch[1].GetSelection()) + 1
                EqpConfig[eqp]['_GPIB'][0] = None
                EqpConfig[eqp]['_IP'][0] = None
            else:
                EqpConfig[eqp]['_COM'] = int(ch[1].GetSelection()) + 1
                EqpConfig[eqp]['_GPIB'] = None
                EqpConfig[eqp]['_IP'] = None
            for each in (0,2,3,4,5,6):
                ch[each].SetSelection(-1)
                    
        elif event_id in (ch[2].GetId(), ch[3].GetId(), ch[4].GetId(), ch[5].GetId()): ##id's for all four ip slots plus one port.
            ip_address = ch[2].GetStringSelection()+"."+ch[3].GetStringSelection()+"."+ch[4].GetStringSelection()+"."+ch[5].GetStringSelection()+ " " +ch[6].GetStringSelection()
            if eqp == 'pos':
                EqpConfig[eqp]['_IP'][0] = ip_address
                EqpConfig[eqp]['_GPIB'][0] = None
                EqpConfig[eqp]['_COM'][0] = None
            else:
                EqpConfig[eqp]['_IP'] = ip_address
                EqpConfig[eqp]['_GPIB'] = None
                EqpConfig[eqp]['_COM'] = None                
            for each in (0,1):
                ch[each].SetSelection(-1)

    def OnChoice(self,event):
        event_id = event.GetId()
        if event_id in [each.GetId() for each in self.ch1]:
            self._OnChoice(event_id, 'vna', self.ch1)
        elif event_id in [each.GetId() for each in self.ch2]:
            self._OnChoice(event_id, 'spe', self.ch2)
        elif event_id in [each.GetId() for each in self.ch3]:
            self._OnChoice(event_id, 'pos', self.ch3)

        
    def OnButton(self,event):
        if event.GetId()==self.but1.GetId():
            self.selected_ctrl = 'vna'
            self.SetupVna()
        elif event.GetId()==self.but2.GetId():
            self.selected_ctrl = 'spe'
            pass
        elif event.GetId()==self.but3.GetId():
            self.SetupPos()
            self.selected_ctrl = 'pos'
        else:
            pass

    def _CrtCommunicationForm(self, Idch, parent):
        """Private method to create address entry form to include gpib, com and ip interfaces."""
        PortAddress = [str(each) for each in range(10000)]
        IPAddress = [str(each) for each in range(256)]
        ComList = [str(each+1) for each in range(256)]
        choice_gpib=wx.Choice(parent, id=Idch[0], choices=AddressList)
        choice_com=wx.Choice(parent, id=Idch[1], choices=ComList)
        choiceip_1=wx.Choice(parent, id=Idch[2], choices=IPAddress)
        choiceip_2=wx.Choice(parent, id=Idch[3], choices=IPAddress)
        choiceip_3=wx.Choice(parent, id=Idch[4], choices=IPAddress)
        choiceip_4=wx.Choice(parent, id=Idch[5], choices=IPAddress)
        choiceip_port=wx.Choice(parent, id=Idch[5], choices=PortAddress)        
#        for each in [choiceip_1, choiceip_2, choiceip_3, choiceip_4, choiceip_port]:
#            each.SetStringSelection('1')
        choice_com.Hide()
        choiceip_1.Hide()
        choiceip_2.Hide()
        choiceip_3.Hide()
        choiceip_4.Hide()
        choiceip_port.Hide()        
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(choice_gpib,0,wx.TOP,border=13)
        sizer.Add(choice_com,0, wx.TOP, border=13)
        sizer.Add(choiceip_1,0, wx.TOP, border=13)
        sizer.Add(choiceip_2,0, wx.TOP, border=13)
        sizer.Add(choiceip_3,0, wx.TOP, border=13)
        sizer.Add(choiceip_4,0, wx.TOP, border=13)
        sizer.Add(choiceip_port,0, wx.TOP|wx.LEFT, border=13 )       
        comm_choice = [choice_gpib, choice_com, choiceip_1, choiceip_2, choiceip_3, choiceip_4, choiceip_port]
#        for each in comm_choice:
 #           each.Bind(wx.EVT_CHOICE, self.OnChoice)
            #self.Bind(wx.EVT_CHOICE, self.OnChoice, each)            
        return sizer, comm_choice
        
    def _CrtCombo(self, caption, Idch, Idbu):
        """Private method to create equipment selection, plus address slection combo widget."""
        sxy=(185,30)
        button=wx.Button(self.panel,Idbu,caption,size=(sxy[0]-20,sxy[1]),style=wx.BU_LEFT)
        textctrl=wx.TextCtrl(self.panel,id=-1,value='Insert New Equipment',size=sxy,style=wx.TE_READONLY)
        comm_sizer, comm_choice = self._CrtCommunicationForm(Idch, self.panel)
        for each in comm_choice:
            each.Bind(wx.EVT_CHOICE, self.OnChoice)
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(button, 0, wx.ALL, border=10)
        sizer.Add(textctrl, 0, wx.ALL, border=10)
        sizer.Add(comm_sizer, 0, wx.BOTTOM, border=10)

        self.combo_sizer = sizer
        self.Bind(wx.EVT_BUTTON, self.OnButton, button)        
        return button, textctrl, comm_choice, sizer


    def _Change_GPIB_Form(self, mode = 'ip'):
        if self.selected_ctrl == 'vna':
            ch = self.ch1
        elif self.selected_ctrl == 'spe':
            ch = self.ch2
        else:
            ch = self.ch3
        self.Change_GPIB_Form(self.panel, mode, ch)
            
    def Change_GPIB_Form(self, the_panel, mode, ch):  ##ch is the list of 7 wx.CHOICES widgets.
        if mode == 'ip':
            for k, each in enumerate(ch):
                if k in (2,3,4,5,6):
                    each.Show()
                else:
                    each.Hide()#self.equipment_sizer.Hide(each)
        elif mode == 'gpib':
            for k, each in enumerate(ch):
                if k == 0:
                    each.Show()#self.equipment_sizer.Show(each)
                else:
                    each.Hide()#self.equipment_sizer.Hide(each)
        elif mode == 'com':
            for k, each in enumerate(ch):
                if k == 1:
                    each.Show()#self.equipment_sizer.Show(each)
                else:
                    each.Hide()#self.equipment_sizer.Hide(each)
        else:
            pass
        the_panel.Layout()


        
        
#Class SetupVna defineds the frame interface for VNA advanced setup.  Class Adv_Vna defines all the handlers from the events triggered within SetupVna frame.
    def SetupVna(self):
        ## Instanstiate the frame from CrtWiget.py.
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
        ## Instantiate the frame from CrtWidget.py.
        telf=Adv_Pos(self,frametitle='Advanced Setup: Positioner')
        telf.parent=self
        telf.panel.SetBackgroundColour((230, 255, 222))
        
        NumberList = ['0','1','2']
        AddressList = [str(x) for x in range(31)]
        AddressList.append('None')
        #Do the frame layout.
        telf.t0, telf.c0, s0, chid0 = telf.TextandChoice('Number of devices to control?', ChoiceList=NumberList)
        telf.t2 = wx.StaticText(telf.panel, -1, pos = (-1, -1), label = "  Address of the second positioner:")

        ### telf.c2 is the list of 7 wx.CHOICES widgets for Adv_Pos frame.
        s2, telf.c2 = self._CrtCommunicationForm([wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId()], telf.panel)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(telf.t2, 0, wx.TOP, border = 15)
        sizer1.Add(s2, 0, wx.ALL, border = 5)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        for each in (s0, sizer1):
            sizer2.Add(each, 0, wx.ALL, border=10)
        telf.panel.SetSizer(sizer2)
        sizer2.Fit(telf.panel)

        ## Add 2nd ctrl selection.
        telf.t2_ctrl, telf.c2_ctrl, ch2id_ctrl = telf.TextandChoice1('Communication (2nd):', ChoiceList = ['GPIB', 'COM', 'IP'], pxy = (15, 130), deltax = 150)
        telf.Bind(wx.EVT_CHOICE, telf.Change_ctrl_pos2, telf.c2_ctrl)
        
        ## Start the initial updates.
        telf.InitUpdate()       
        ## Binding to automatically update the EqpConfig list from the choice boxes. 
        telf.Bind(wx.EVT_CHOICE, telf.Update0, telf.c0)
        for each in telf.c2:
            telf.Bind(wx.EVT_CHOICE, telf.On_c2_Choice, each)
            
        telf.Bind(wx.EVT_CLOSE, telf.OnClose)
        telf.Show()
        


        

class Adv_Common(CrtFrame):
    def __init__(self, parent, frametitle):
        CrtFrame.__init__(self, parent, frametitle, sxy = (500, 400))
        self.parent = parent
        self.t_ctrl, self.c_ctrl, chid_ctrl = self.TextandChoice1('Communication type:', ChoiceList = ['GPIB', 'COM', 'IP'], pxy = (15, 300), deltax = 150)
        self.Bind(wx.EVT_CHOICE, self.Change_ctrl, self.c_ctrl)        

    def Change_ctrl(self, event):
        equip_name = self.__class__.__name__[-3:].lower()
        self.ctrl_type = str(self.c_ctrl.GetStringSelection())
        self.parent._Change_GPIB_Form(mode = self.ctrl_type.lower())
        EqpConfig[equip_name]['_CTRL1'] = self.ctrl_type
            


class Adv_Pos(Adv_Common):
    def InitUpdate(telf):  #Restore the parameters from EqpConfig list
        telf.c_ctrl.SetStringSelection(EqpConfig['pos']['_CTRL1'])
        telf.c2_ctrl.SetStringSelection(EqpConfig['pos']['_CTRL2'])
        if EqpConfig['pos']['nod'] != None: telf.c0.SetSelection(EqpConfig['pos']['nod'])
        #if EqpConfig['pos']['_GPIB'][0] != None: telf.c1.SetSelection(EqpConfig['pos']['_GPIB'][0])
        if EqpConfig['pos']['_GPIB'][1] != None: telf.c2[0].SetSelection(EqpConfig['pos']['_GPIB'][1])
        if EqpConfig['pos']['_COM'][1] != None: telf.c2[1].SetSelection(EqpConfig['pos']['_COM'][1])
        if EqpConfig['pos']['_IP'][1] != None:
            ip_address, port_number = EqpConfig['pos']['_IP'][1].split(" ")
            ip_address = ip_address.split(".")
            telf.c2[6].SetSelection(int(port_number))
            for each in (2,3,4,5):
                telf.c2[each].SetSelection(int(ip_address[each-2]))
                                                                                                
        if EqpConfig['pos']['_CTRL2'] == 'GPIB':
            telf.parent.Change_GPIB_Form(telf.panel, 'gpib', telf.c2) ##telf.c2 is the list of 7 wx.CHOICES widgets.
        elif EqpConfig['pos']['_CTRL2'] == 'COM':
            telf.parent.Change_GPIB_Form(telf.panel, 'com', telf.c2)
        elif EqpConfig['pos']['_CTRL2'] == 'IP':
            telf.parent.Change_GPIB_Form(telf.panel, 'ip', telf.c2)
                                        
    def Change_ctrl_pos2(telf, event):
        selection = telf.c2_ctrl.GetStringSelection()
        EqpConfig['pos']['_CTRL2'] = str(selection)
        telf.parent.Change_GPIB_Form(telf.panel, selection.lower(), telf.c2) ##telf.c2 is the list of 7 wx.CHOICES widgets.
        
    def On_c2_Choice(telf, event):
        ch = telf.c2
        event_id = event.GetId()
        if event_id == ch[0].GetId():
            EqpConfig['pos']['_GPIB'][1] = int(ch[0].GetSelection())
            EqpConfig['pos']['_COM'][1] = None
            EqpConfig['pos']['_IP'][1] = None
            for each in (1,2,3,4,5,6):
                ch[each].SetSelection(-1)
                
        elif event_id == ch[1].GetId():
            EqpConfig['pos']['_COM'][1] = int(ch[1].GetSelection()) + 1
            EqpConfig['pos']['_GPIB'][1] = None
            EqpConfig['pos']['_IP'][1] = None
            for each in (0,2,3,4,5,6):
                ch[each].SetSelection(-1)
        else:
            ip_address = ch[2].GetStringSelection()+"."+ch[3].GetStringSelection()+"."+ch[4].GetStringSelection()+"."+ch[5].GetStringSelection()+ " " +ch[6].GetStringSelection()
            EqpConfig['pos']['_IP'][1] = ip_address
            EqpConfig['pos']['_GPIB'][1] = None
            EqpConfig['pos']['_COM'][1] = None
            for each in (0,1):
                ch[each].SetSelection(-1)

                                                            
    def Update0(telf, event):
        selection = telf.c0.GetSelection()
        EqpConfig['pos']['nod'] = selection
        if selection == 2:
            telf.t2_ctrl.Show()
            telf.c2_ctrl.Show()
        else:
            telf.t2_ctrl.Hide()
            telf.c2_ctrl.Hide()
        telf.Layout()
            
    def Update1(telf,event):
        EqpConfig['pos']['_GPIB'][0]=eval(telf.c1.GetStringSelection())
        telf.parent.ch3[0].SetSelection(EqpConfig['pos']['_GPIB'][0])

    def Update2(telf,event):
        EqpConfig['pos']['_GPIB'][1]=eval(telf.c2.GetStringSelection())
        
    def OnClose(telf,event):  #Use OnClose method to check the input parameters.
        ctrl1_non_used = lambda a, b, c : (not a[0])+(not b[0])+(not c[0])
        ctrl2_non_used = lambda a, b, c : (not a[1])+(not b[1])+(not c[1])        

        non_ctrl1 = ctrl1_non_used(EqpConfig['pos']['_GPIB'], EqpConfig['pos']['_COM'], EqpConfig['pos']['_IP'])
        non_ctrl2 = ctrl2_non_used(EqpConfig['pos']['_GPIB'], EqpConfig['pos']['_COM'], EqpConfig['pos']['_IP'])        
        
        
        if (non_ctrl1 + non_ctrl2) == 0 and EqpConfig['pos']['nod'] == None:
            pass

        elif non_ctrl1 == 0 and EqpConfig['pos']['nod'] == 1:
            dlg=wx.MessageDialog(telf,"Warning: No address assigned to the 1st positioner!",style=wx.OK)
            dlg.ShowModal()
            
        elif non_ctrl2 == 0 and EqpConfig['pos']['nod'] == 2:
            dlg=wx.MessageDialog(telf,"Warning: No address assigned to the 2nd positioner!",style=wx.OK)
            dlg.ShowModal()
        else:
            pass

        if ((EqpConfig['pos']['_GPIB'][0] != None) and (EqpConfig['pos']['_GPIB'][0]==EqpConfig['pos']['_GPIB'][1]) or
            (EqpConfig['pos']['_GPIB'][1] != None) and (EqpConfig['pos']['_GPIB'][1]==EqpConfig['pos']['_GPIB'][2]) ):
            dlg=wx.MessageDialog(telf,"Warning: Duplicate GPIB address!",style=wx.OK)
            dlg.ShowModal()
            flag_close=0
            
        telf.Destroy()




                              
class Adv_Vna(Adv_Common):
    def InitUpdate(telf):
        telf.c_ctrl.SetStringSelection(EqpConfig['vna']['_CTRL1'])        
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
        
