import wx
from MeaCase import *
import pickle
from CrtWidget import *
from MeaLibrary import *
##import wx.lib.stattext
##wx.StaticText=wx.lib.stattext.GenStaticText


    
class MeaTreeFrame(CrtTreeFrame):
    underconstructedFlag=0;
    def __init__(self,parent):  #This parent refers to the MainGUI frame.
        CrtTreeFrame.__init__(self,parent,frametitle='Expand the tree and double-click to add measurement item.',img=("icon1.bmp","icon2.bmp"),spdistance=350,sxy=(850,600),rootlabel='Measurement',treelist=MeaList)

        self._DoLayout()
### (to be coded later)        self.Bind(wx.EVT_BUTTON,self.OnSetupButton,self.setupbutton)        
        self.Show()

    def _DoLayout(self):
        self.panel.SetBackgroundColour(c_silver) 
        self.meatext=wx.StaticText(self.panel,-1,'Measurement Type:',pos=(7,10))
        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.meatext.SetFont(font)        
        self.text=wx.StaticText(self.panel,-1,'Enter Measurement Title:',pos=(8,40))
        self.entername=wx.TextCtrl(self.panel,-1,'New Test',pos=(6,60),size=(180,24))
### (to be coded later)       self.setupbutton=wx.Button(self.panel,-1,'Measurement Detailed Setup',pos=(6,500),size=(320,24))
        self.dscrpt=wx.StaticText(self.panel,-1,'Description:',pos=(7,150))
        self.descrptbox=wx.TextCtrl(self.panel,-1,pos=(7,170),size=(450,200),style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.dscrpt.SetFont(font)
 

    def __del__(self):  #When the frame is closed, all the equipment settings are written into eqpsetup.ini.
        self.parent.Enable(True)
            
    def OnSetupButton(self,event):
        if not MeaTreeFrame.underconstructedFlag:
            self.SetupFrame()

    def OnClick(self,event):  #ctrl-tree event of single click
        self.selectedType=self.tree.GetItemText(event.GetItem())
        self.selectedID=MeaID[self.selectedType]

        if self.selectedID>100:
            self.meatext.SetLabel('Test Case %s' % self.selectedType)
        elif self.selectedID>10:
            self.meatext.SetLabel('Category Group %s' % self.selectedType)
        else:
            self.meatext.SetLabel('Measurement Category %s' % self.selectedType)
                
        try:
            MeaTreeFrame.underconstructedFlag=0
            self.descrptbox.SetValue('%s' % eval('meadscrp.content'+str(self.selectedID)))
        except:
            MeaTreeFrame.underconstructedFlag=1               
            self.descrptbox.SetValue('Under Construction!')
                
        
    def OnDClick(self,event):#ctrl-tree event of double click
        selectedType=self.tree.GetItemText(event.GetItem())
        selectedID=MeaID[selectedType]
        name=self.entername.GetValue()
        ## This self.parent refers to the MainGUI frame.
        eval('CrtMea'+str(selectedID))(self.parent, selectedType, selectedID, name)
 

    def SetupFrame(self):
        telf=AdvSetup(self,frametitle='Detailed Setup:%s' % self.selectedType)
        telf.panel.SetBackgroundColour(c_silver)

        #Doing the iterative layout.
        #print self.selectedID
        #print str(self.selectedID)
        #print MeaConfig[str(self.selectedID)]
        #print MeaConfig[str(self.selectedID)]['para']
        telf.number=len(MeaConfig[str(self.selectedID)]['para'])

        n=0
        telf.itemlist=[]#This is the list to store all the triples of (text, choice, sizer, choiceid) from the returns of TextandChoice method.
        for each in MeaConfig[str(self.selectedID)]['para']:
            #print SetupQuestion()[str(self.selectedID)]['questions'][n]
            #print SetupQuestion()[str(self.selectedID)]['choices'][n]                  
            telf.itemlist.append(telf.TextandChoice(SetupQuestion()[str(self.selectedID)]['questions'][n],SetupQuestion()[str(self.selectedID)]['choices'][n]))
            n+=1
    
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizerlist=[telf.itemlist[x][2] for x in range(telf.number)]
        map((lambda x: sizer.Add(x,0,wx.ALL,border=5)),sizerlist)
        #Binding event through map function.
        telf.choicelist=[telf.itemlist[x][1] for x in range(telf.number)]
        map((lambda x: telf.Bind(wx.EVT_CHOICE,telf.OnChoice,x)),telf.choicelist)
            
        telf.panel.SetSizer(sizer)
        sizer.Fit(telf.panel)
        telf._Update()
        telf.Show()


        
class AdvSetup(CrtFrame):  #This is the frame to be called for detailed setup in each measurement type.
    def OnChoice(telf,event):
        exclusive={'Theta':'Phi','Phi':'Theta'}
        idlist=[telf.itemlist[x][3] for x in range(telf.number)]
        n=0
        for each in idlist:
            if event.GetId()==each:
                selected=telf.choicelist[n].GetStringSelection()
                if exclusive.has_key(selected):
                    for each2 in telf.choicelist:
                        if each2!=telf.FindWindowById(each) and each2.GetStringSelection()==selected:
                            each2.SetStringSelection(exclusive[selected])
                break
            else:
                n=n+1
        for n in range(telf.number):
            MeaConfig[str(telf.parent.selectedID)]['value'][n]=telf.choicelist[n].GetStringSelection()           


    def __init__(telf,parent,frametitle):
        telf.parent=parent
        CrtFrame.__init__(telf,parent,frametitle,sxy=(500,450))
#        telf.visacodes=wx.TextCtrl(telf.panel,-1,'Enter additional VISA codes herein.  \nFor example: vna(*IDN?)\n\nCodes are seperated by comma or newline.  \nFor example: vna(*IDN?),spe(*IDN?)',size=(360,150),pos=(10,250),style=wx.TE_MULTILINE)
        
    def __del__(telf):
        CrtFrame.__del__(telf)
        setupfile=open('measetup.ini','wb')
        pickle.dump(MeaConfig,setupfile)
        setupfile.close()


    def _Update(telf):
        setupfile=open('measetup.ini','rb')
        MeaConfig=pickle.load(setupfile)
        setupfile.close()
 
        n=0
        for each in MeaConfig[str(telf.parent.selectedID)]['value']:
            telf.itemlist[n][1].SetStringSelection(each)
            n+=1


#The following is the list of descriptions to explain the details of each measurement type.









    
