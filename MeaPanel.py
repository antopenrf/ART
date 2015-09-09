import os

import wx
import wx.grid  
import wx.lib.masked.numctrl
NumCtrl=wx.lib.masked.numctrl.NumCtrl

from admin import *
from CrtWidget import *
import MeaDB
import MeaPlot



#MeaPanel is the superclass that will be inherited by all children(which are named after meaID) measurement panels.
class MeaPanel(wx.MDIChildFrame):
    sp1pos=550
    sp1adv=800
    count=0
    advflag=0

    def __init__(self, parent, title):  
        ## This parent is the MainGUI frame.
        ## 'self' referes to the MeaPanel Frame itself; parent here refers to the Main GUI frame.
        wx.MDIChildFrame.__init__(self, parent, -1, title, size=(750,600))
##         MeaPanel.count+=1
## Move this count under CrtMea000 of MeaCase.py.
        self.parent = parent                
        self._LayoutMain()
        self._LayoutAdvanced()

        ## Create measurement frame icon.
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("mea.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        ## The Run Button is given here in the parent MeaPanel class.
        self.panelW.RunBut=wx.Button(self.panelW,-1,'Run',size=(180,30))        
        self.panelW.Bind(wx.EVT_BUTTON,self.OnRunBut,self.panelW.RunBut)

        ## Bind the EVT_CLOSE event.
        self.Bind(wx.EVT_CLOSE,self.Close)


        
    def _LayoutMain(self):
        """Private method: main measurement panel layout."""
        ## Set#  the splitter window(left and right), left: meausurement parameters, right: plot
        self.sp1 = wx.SplitterWindow(self)
        self.scrollA = wx.ScrolledWindow(self.sp1,-1) ## The left part: scroll window.
        self.scrollA.SetScrollbars(1,1,100,965)
        self.scrollA.SetScrollRate(15,15)     
        self.panelW = wx.Panel(self.scrollA, style=wx.SUNKEN_BORDER)  ## wx.Panel addes onto the scroll window.
        self.panelW.SetBackgroundColour(c_silver)
        self.plotter = MeaPlot.Figure2D(self.sp1)     ## The right part: Matplotlib figure instance
        self.sp1.SplitVertically(self.scrollA, self.plotter)
        self._SetSplitter(self.sp1, MeaPanel.sp1pos)

        ## Bind a method to make the sash unmovable
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED,self._OnSashChanged1,self.sp1)


    def Close(self,event):
        # The meaDB instance will be removed from the database list.  Also remove from the project tree.
        self.parent.projtree.SetItemTextColour(self.meadb.treeID,c_lightblue2)
        self.Hide()


    def _LayoutAdvanced(self):
        #Set the engineer mode control button.
        wx.StaticLine(self.panelW,-1,pos=(MeaPanel.sp1pos,4),size=(2,1800),style=wx.LI_VERTICAL)
        self.panelW.ModeBut=self.CrtModeBut(self.panelW)
        self.panelW.ModeBut.Hide()
        text1 = wx.StaticText(self.panelW,-1,pos=(220,10),label='Measurement Setting')
        text2 = wx.StaticText(self.panelW,-1,pos=(220,310),label='Equipment Setting')
        text3 = wx.StaticText(self.panelW,-1,pos=(220,610),label='Information')        

        font = wx.Font(gfontsize, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        text1.SetFont(font)
        text2.SetFont(font)
        text3.SetFont(font)        

        self.ts1 = wx.StaticText(self.panelW, -1, 'Test Title:', pos=(220, 640))
        self.tcs1= wx.TextCtrl(self.panelW, -1, pos=(218, 655), size=(300, 20), style=wx.TE_LEFT)

        self.ts5 = wx.StaticText(self.panelW, -1, 'Operator Name:', pos=(220, 680))
        self.tcs5= wx.TextCtrl(self.panelW, -1, pos=(218, 695), size=(300, 20), style=wx.TE_LEFT)
        
        self.ts6 = wx.StaticText(self.panelW, -1, 'Comments:', pos=(220,845))
        self.tcs6= wx.TextCtrl(self.panelW, -1, pos=(218, 860), size=(300, 100), style=wx.TE_LEFT|wx.TE_MULTILINE)
        
        self.ts7 = wx.StaticText(self.panelW, -1,'Testing Update:', pos=(220,720))
        self.tcs7= wx.TextCtrl(self.panelW, -1, pos=(218, 735), size=(300,100), style=wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY)

        for each in [self.tcs1, self.tcs5, self.tcs6, self.tcs7]:
            self.panelW.Bind(wx.EVT_TEXT, self._OnInfoChange, each)
        
        lineH1 =wx.StaticLine(self.panelW,-1,size=(540,2),pos=(210,300),style=wx.LI_HORIZONTAL)
        lineH2 =wx.StaticLine(self.panelW,-1,size=(540,2),pos=(210,600),style=wx.LI_HORIZONTAL)          
        lineV =wx.StaticLine(self.panelW,-1,size=(2,980),pos=(195,10),style=wx.LI_VERTICAL)


    def _OnInfoChange(self, event):
        self.meadb.testname = self.tcs1.GetValue()
        self.meadb.operatorname = self.tcs5.GetValue()
        self.meadb.comments = self.tcs6.GetValue()
        self.meadb.testinglog = self.tcs7.GetValue()
                                     
            
    def GeneMeaDB(self,meatype,meaID,count,name):
        #### ---- Important -----
        #### ---- self.meadb is the object the stores all the data and parameters that are associated with the current MeaPanel.
        self.meadb = MeaDB.MeadbGenerator(self, meatype, meaID, count, name)
        MeaDB.DBadd(self.meadb)
        self.meadb.treeID = self.projtree.AddMeaItem(self.meadb.meaname)

        
    def _OnSashChanged1(self,event):
        if MeaPanel.advflag==0:
            self.sp1.SetSashPosition(MeaPanel.sp1pos)
        elif MeaPanel.advflag==1:
            self.sp1.SetSashPosition(MeaPanel.sp1adv)
        else: pass

##    def _OnSashChanged2(self,event):
##        pixels = tuple (self.GetClientSize())
##        self.sp2.SetSashPosition(pixels[1]*0.5,redraw=True)   
       

    def _SetSplitter(self,splitter,pos,minpos=150):
        splitter.SetMinimumPaneSize(minpos)
        splitter.SetSashPosition(pos,redraw=True)

        
    #statictext and numeric control box as basic contructing element
    def TextandNumCtrl(self,telf,label,sx=60):
        text=wx.StaticText(telf,-1,label, size=(-1,-1), style=wx.TE_LEFT)
        font = wx.Font(gfontsize, gfont_para, wx.NORMAL,wx.NORMAL)
        text.SetFont(font)        
        nctrl=NumCtrl(telf,-1,size=wx.DefaultSize,pos=wx.DefaultPosition,style=wx.ALIGN_LEFT,value = 0,fractionWidth = 2 , max = 100000)
        telf.sizer=wx.BoxSizer(wx.VERTICAL)
        telf.sizer.Add(text,0,0,border=0)
        telf.sizer.Add(nctrl,0,0,border=0)
        return text,nctrl,telf.sizer
    
    def TextandTextCtrl(self,relf,label,sx=300,sy=-1,textstyle=wx.TE_LEFT):
        text=wx.StaticText(relf,-1,label,size=(sx,-1),style=wx.TE_LEFT)
        font = wx.Font(gfontsize, gfont_para, wx.NORMAL,wx.NORMAL)
        text.SetFont(font)        
        tctrl=wx.TextCtrl(relf,-1,size=(sx,sy),style=textstyle)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text,0,wx.ALL,border=2)
        sizer.Add(tctrl,0,wx.ALL,border=2)
        return text,tctrl,sizer
    
#self refers to the MeaPanel Frame; telf refers to the panelW(telf=self.panelW).    
    def CrtFreqEntry(self,telf):
##        line =wx.StaticLine(telf,-1,size=(200,2),style=wx.LI_HORIZONTAL)  
        head = CrtBoldText(telf,'Frequency Setup',gfontsize,c_blue)      
        telf.RB=wx.RadioBox(telf,-1,'      Entry Method      ',(-1,-1),wx.DefaultSize,['Start/Stop/Step','Single Frequency','Import From List'],majorDimension=3,style=wx.RA_SPECIFY_ROWS)
        telf.t0,telf.nc0,telf.s0=self.TextandNumCtrl(telf,'Start (MHz) ')
        telf.t1,telf.nc1,telf.s1=self.TextandNumCtrl(telf,'Stop (MHz) ')
        telf.t2,telf.nc2,telf.s2=self.TextandNumCtrl(telf,'Step (MHz) ')
        telf.sizer0=wx.BoxSizer(wx.VERTICAL)        #sizer0
        for each in [telf.s0,telf.s1,telf.s2]:
            telf.sizer0.Add(each,0,wx.ALL,border=2)
   
        telf.t3,telf.nc3,telf.s3=self.TextandNumCtrl(telf,'Single(MHz) ')
        telf.sizer1=wx.BoxSizer(wx.VERTICAL)        #sizer1
        telf.sizer1.Add(telf.s3,0,wx.ALL,border=2)
 
        telf.sizer2=wx.BoxSizer(wx.VERTICAL)        #sizer2
        telf.but=wx.Button(telf,-1,'Browse File')
        telf.sizer2.Add(telf.but,0,wx.ALL,border=5)
        telf.sizer012=wx.BoxSizer(wx.VERTICAL)      #sizer012=sizer0 + 1 + 2 in vertical
        for each in [telf.sizer0,telf.sizer1,telf.sizer2]:
            telf.sizer012.Add(each,0,wx.ALL,border=2)        

        #Use the vertical staticline to get the space fixed in y direction for the three frequency widgets.
        #In this way, when we use Hide() method to only show one of the three, the entire sizer won't change from time to time.
        telf.lineV=wx.StaticLine(telf,-1,size=(0,150),style=wx.LI_VERTICAL)
        telf.sizer3=wx.BoxSizer(wx.HORIZONTAL)      #sizer3 is to hold up sizer012 with a vertical line.
        telf.sizer3.Add(telf.lineV,0,wx.ALL,border=2)           #So, sizer3 contains sizer0,sizer1 and sizer2.
        telf.sizer3.Add(telf.sizer012,0,wx.ALL,border=2)
        telf.sizer012.Hide(self.panelW.sizer1)
        telf.sizer012.Hide(self.panelW.sizer2)
 
        butwidth=int(200/3)-12
        telf.FreqAdd=wx.Button(telf,-1,'Add',size=(butwidth,30))
        telf.FreqRemove=wx.Button(telf,-1,'Del',size=(butwidth,30))
        telf.FreqClear=wx.Button(telf,-1,'Clear',size=(butwidth,30))
 
        telf.sizer4=wx.BoxSizer(wx.HORIZONTAL)      #sizer4 is the three frequency botton sizer.
        for each in [telf.FreqAdd,telf.FreqRemove,telf.FreqClear]:
            telf.sizer4.Add(each,0,wx.ALL,border=0)              


        telf.FreqChkBox=wx.CheckListBox(telf,-1,pos=(13,280),size=(butwidth*3,400))

        #Add all frequency widgets uner one sizer, named 'sizer'.
        telf.sizer=wx.BoxSizer(wx.VERTICAL)
        telf.nof_text = wx.StaticText(telf, -1, label = "points", pos = (20, 100), size = (-1, -1), style=wx.TE_LEFT)
        for each in [head, telf.RB, telf.sizer3, telf.nof_text, telf.sizer4, telf.FreqChkBox]:
            telf.sizer.Add(each,0,wx.ALIGN_CENTER|wx.ALL,2)               
    
        self.Bind(wx.EVT_RADIOBOX,self.OnFreqRadio,telf.RB)          
        self.Bind(wx.EVT_BUTTON,self.OnFreqAdd,telf.FreqAdd)
        self.Bind(wx.EVT_BUTTON,self.OnFreqRemove,telf.FreqRemove)
        self.Bind(wx.EVT_BUTTON,self.OnFreqClear,telf.FreqClear)        
        return telf.sizer

    def OnFreqAdd(self,event):
        RB=self.panelW.RB.GetSelection()
        start=self.panelW.nc0.GetValue()
        stop=self.panelW.nc1.GetValue()
        step=self.panelW.nc2.GetValue()
        single=self.panelW.nc3.GetValue()
        if RB==0:
            if start==0:
                WarningFrame('Wanring: start frequency can not be zero !')
            elif stop==0: WarningFrame('Wanring: stop frequency can not be zero !')
            elif step==0 and start!=stop: WarningFrame('Wanring: step frequency can not be zero !')
            else: pass

            if stop==start: pass
            elif stop<start: WarningFrame('Warning: stop frequency can not be smaller than start frequency !')
            elif (stop-start)<step: WarningFrame('Warning: step frequency must be smaller than (stop-start) !')
        
            def freq(start,stop,step):
                if start==stop and start!=0:
                    return [start]
                
                elif step!=0 and stop>start:
                    freqlist=[]
                    n=0
                    f=start
                    while f<=stop:
                        freqlist.append(f)
                        n=n+1
                        f=start+step*n
                    return freqlist
                else:
                    return []
                
            entered=freq(start,stop,step)

        if RB==1: # the case with single frequency
            if single==0:
                WarningFrame('Wanring: entered frequency can not be zero !')
                entered=[]
            else:
                entered=[single]
        if RB==2:
            entered=[]
            print 'under construction'
        self.meadb.iFreq=list(set(entered)|set(self.meadb.iFreq))
        self.UpdateFreqChkBox()

        
    def UpdateFreqChkBox(self):    
        # update the checkbox list     
        self.meadb.iFreq.sort()
        self.panelW.FreqChkBox.Clear()
        n=0
        for x in self.meadb.iFreq:
            self.panelW.FreqChkBox.Append(str(x)+' '+'MHz'+' '*2+'('+str(n+1)+')')
            self.panelW.FreqChkBox.Check(n, check=True)
            n+=1
        self.plotter.drawxlimit(self.meadb.iFreq)
        self.panelW.nof_text.SetLabel(str(len(self.meadb.iFreq)) + " points")
        self.panelW.Update()

        
    def OnFreqRemove(self,event):
        inmeadb=self.meadb.iFreq
        number=len(inmeadb)
        for x in range(number):
            if not self.panelW.FreqChkBox.IsChecked(x):
                self.meadb.iFreq.remove(inmeadb[x])
        self.UpdateFreqChkBox()

    def OnFreqClear(self,event):
        self.panelW.FreqChkBox.Clear()
        self.meadb.iFreq=[]
        
    def OnFreqRadio(self,event):
        if event.GetSelection()==0:
            self.panelW.sizer012.Show(self.panelW.sizer0)
            self.panelW.sizer012.Hide(self.panelW.sizer1)
            self.panelW.sizer012.Hide(self.panelW.sizer2)
            self.panelW.Layout()
            
        elif event.GetSelection()==1:
            self.panelW.sizer012.Show(self.panelW.sizer1)
            self.panelW.sizer012.Hide(self.panelW.sizer0)
            self.panelW.sizer012.Hide(self.panelW.sizer2)
            self.panelW.Layout()

        else:
            self.panelW.sizer012.Show(self.panelW.sizer2)
            self.panelW.sizer012.Hide(self.panelW.sizer1)
            self.panelW.sizer012.Hide(self.panelW.sizer0)
            self.panelW.Layout()            
  
    def CrtModeBut(self,telf):
        telf.ModeBut=wx.ToggleButton(telf,-1,'Engineer Mode',size=(MeaPanel.sp1pos-20,30),pos=(-1,945))        
        telf.Bind(wx.EVT_TOGGLEBUTTON,self.OnModeBut,telf.ModeBut)
        return telf.ModeBut
        
    def OnModeBut(self,event):
        password=PwdCtrl()
        telf=self.panelW
        finalpos=MeaPanel.sp1adv 
        span=finalpos-MeaPanel.sp1pos
        resolution=58
        if telf.ModeBut.GetValue()==True:
            MeaPanel.advflag=1
            for n in range(span/resolution+1):
                self.sp1.SetSashPosition(MeaPanel.sp1pos+resolution*n)
            telf.ModeBut.SetLabel('Quick Mode')
        else:
            MeaPanel.advflag=0            
            for n in range(span/resolution+1):
                self.sp1.SetSashPosition(finalpos-resolution*n)
            telf.ModeBut.SetLabel('Engineer Mode')

    def CrtOneAxis(self,telf,meadb):
        head = CrtBoldText(telf, 'Positioner Setup', gfontsize, c_blue)                 
        config = meadb.iPara
        meaid = str(meadb.meaID)
        line = wx.StaticLine(telf,-1,size=(160,2), style=wx.LI_HORIZONTAL)           
        telf.t4, telf.nc4, telf.s4 = self.TextandNumCtrl(telf, config[meaid]['value'][0] + '-Axis Step:')
        telf.t5, telf.nc5, telf.s5 = self.TextandNumCtrl(telf, config[meaid]['value'][2] + '-Axis Position:')
        if self.meadb.iPara[str(self.meadb.meaID)]['value'][1]=='No': telf.nc5.Disable()
        sizer = wx.BoxSizer(wx.VERTICAL)
        telf.Bind(wx.EVT_TEXT, self.OnPrimaryRotation, telf.nc4)
        telf.Bind(wx.EVT_TEXT, self.OnSecondaryFixed, telf.nc5)
        for each in [line,head,telf.s4,telf.s5]:
            sizer.Add(each, 0, wx.ALIGN_CENTER|wx.ALL, 5)          
        return sizer


    def OnPrimaryRotation(self,event):
        self.meadb.iPara[str(self.meadb.meaID)]['_PrimaryStep']=self.panelW.nc4.GetValue()
 
    def OnSecondaryFixed(self,event):
        self.meadb.iPara[str(self.meadb.meaID)]['_SecondaryFixed']=self.panelW.nc5.GetValue()
 
    def AdvTextChoice(self, telf, label, pxy, ChoiceList):
        text = wx.StaticText(telf, -1, label, pos=pxy, style=wx.TE_LEFT)
        font = wx.Font(gfontsize, gfont_para, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)
        newid = wx.NewId()
        choice = wx.Choice(telf, id=newid, pos=(pxy[0]+170, pxy[1]-5), choices=ChoiceList)
        return text, choice, newid

    def CrtCorrectionBrowser1(self,telf,text,pos):
        button=wx.Button(parent=telf,id=-1,label=text,pos=pos,size=(200,-1))
        self.b1_txtctrl=wx.TextCtrl(parent=telf,id=-1,pos=(pos[0],pos[1]+30),size=(330,-1))
        telf.Bind(wx.EVT_BUTTON,self.OnBrowser1Button,button)
        return self.b1_txtctrl

    def OnBrowser1Button(self,event):
        telf=self.panelW        
        dialog=wx.FileDialog(telf,"Choose the correction file",os.path.join(os.getcwd(),'rawdata'),"","*.*", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.b1_txtctrl.SetValue(dialog.GetPath())
        
    def CrtCorrectionBrowser2(self,telf,text1,text2,pos):
        button1=wx.Button(parent=telf,id=-1,label=text1,pos=pos,size=(200,-1))
        self.b2_txtctrl1=wx.TextCtrl(parent=telf,id=-1,pos=(pos[0],pos[1]+30),size=(330,-1))
        button2=wx.Button(parent=telf,id=-1,label=text2,pos=(pos[0],pos[1]+60),size=(200,-1))
        self.b2_txtctrl2=wx.TextCtrl(parent=telf,id=-1,pos=(pos[0],pos[1]+90),size=(330,-1))        
        telf.Bind(wx.EVT_BUTTON,self.OnBrowser2Button1,button1)
        telf.Bind(wx.EVT_BUTTON,self.OnBrowser2Button2,button2)        
        return self.b2_txtctrl1,self.b2_txtctrl2

    def OnBrowser2Button1(self,event):
        telf=self.panelW        
        dialog=wx.FileDialog(telf,"Correction for Polarization 1",os.path.join(os.getcwd(),'rawdata'),"","*.*", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.b2_txtctrl1.SetValue(dialog.GetPath()) 
    def OnBrowser2Button2(self,event):
        telf=self.panelW        
        dialog=wx.FileDialog(telf,"Correction for Polarization 2",os.path.join(os.getcwd(),'rawdata'),"","*.*", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.b2_txtctrl2.SetValue(dialog.GetPath()) 
               
    # To be overridden by MeaCase.py
    def OnRunBut(self,event):
        pass
