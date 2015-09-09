## GUI_MAPS.py, starting date: July 26, 2012, written by yulung tang
## This is a simple GUI that controls EMCO2090.
## The import technique about threading is applied herein.
## version 2
## changes: use the device object as the pass-in parameter for SubPanel class.
## In this way, all the if conditions to tell device 1 from 2 can be skimmed.

import wx
import visa
import threading
from positioners import *
import time
import pickle
 
eqpfile=open('EqpConfig.pkl','rb')
EqpConfig=pickle.load(eqpfile)
en=str(EqpConfig['pos']['eqpno'])
Dev1=eval('pos'+en)('theta',EqpConfig['pos']['GPIB'][0])
Dev2=eval('pos'+en)('phi',EqpConfig['pos']['GPIB'][1])

#threading is the important part of the code to real-time display current position info.

class ReportingCP(threading.Thread):
#'ThreadTheta and ThreadPhi are important flags to ensure there is always one thread running to update current position on GUI display

    def __init__(self,window,device):
        threading.Thread.__init__(self)
        self.window=window
        self.device=device
        self.start()
        self.device.flagOPC=1         
        
    def run(self):
        while not self.device.ifopc():
            self.window.cpbox.SetValue(self.device.current())
        self.device.flagOPC=0

class SubPanel(wx.Panel):
    def __init__(self,parent,device):
        wx.Panel.__init__(self,parent,style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour("yellow")
        self.device=device
        self.__DoLayout()
        self.__DoBinding()
        self.__Starting()

    def __DoLayout(self):
        self.CrtText(self,pos=(10,7),label='Device Current Position')
        
        self.CrtText(self,pos=(10,29),label='%s:' % self.device.name)
        self.zero=self.CrtButton(self,pos=(120,23),label='ZERO',size=(75,25))
        self.cpbox=self.CrtTextCtrl(self,pos=(52,25),size=(60,20))
        
        self.CrtText(self,pos=(10,64),label='Target:')
        self.seek=self.CrtButton(self,pos=(120,59),label='SEEK',size=(75,25))
        self.skbox=self.CrtTextCtrl(self,pos=(52,61),size=(60,20))

        self.CrtText(self,pos=(7,107),label='Upr Limit')
        self.max=wx.Button(self,pos=(2,145),label='Set Upr',size=(60,25))
        self.maxbox=self.CrtTextCtrl(self,pos=(2,123),size=(60,20))

        self.CrtText(self,pos=(69,107),label='Lwr Limit')
        self.min=wx.Button(self,pos=(64,145),label='Set Lwr',size=(60,25))
        self.minbox=self.CrtTextCtrl(self,pos=(64,123),size=(60,20))
        
        self.mvtozero=self.CrtButton(self,pos=(120,90),label='Go 0',size=(75,25))
        self.stop=self.CrtButton(self,pos=(130,122),size=(64,50),label="STOP!")
 
    def CrtText(self,panel,label,pos):
        wx.StaticText(panel,-1,label,pos)

    def CrtButton(self,parent,label,pos,size):
        button=wx.Button(parent,-1,label,pos,size=size)
        return button

    def CrtTextCtrl(self,parent,pos,size):
        textctrl=wx.TextCtrl(parent=parent,id=-1,pos=pos,size=size)
        return textctrl

    def __DoBinding(self):
        self.Bind(wx.EVT_BUTTON,self.SetZero,self.zero)        
        self.Bind(wx.EVT_BUTTON,self.SeekPos,self.seek)
        self.Bind(wx.EVT_BUTTON,self.SetMax,self.max)
        self.Bind(wx.EVT_BUTTON,self.SetMin,self.min)
        self.Bind(wx.EVT_BUTTON,self.StayPut,self.stop)
        self.Bind(wx.EVT_BUTTON,self.GoZero,self.mvtozero)

    def __Starting(self):
        self.cpbox.SetValue(str(self.device.current()))
        self.minbox.SetValue(str(self.device.lwrlmt()))
        self.maxbox.SetValue(str(self.device.uprlmt()))
        
# Give all the handlers in the following.            
    def SetZero(self,event):
        self.device.crtozero()
        self.cpbox.SetValue('0')
        
    def SeekPos(self,event):
        self.device.mvto(self.skbox.GetValue())
        if not self.device.flagOPC:
            self.thread=ReportingCP(self,self.device)
    
    def SetMax(self,event):
        self.device.setuprlmt(self.maxbox.GetValue())

    def SetMin(self,event):
        self.device.setlwrlmt(self.minbox.GetValue())

    def StayPut(self,event):
        self.device.stop()
        
    def GoZero(self,event):
        self.device.mvtozero()
        if not self.device.flagOPC:
            self.thread=ReportingCP(self,self.device)


class MainFrame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'MAPS Navigator',size=(422,213))
        self.sp=wx.SplitterWindow(self)
        self.p1=SubPanel(self.sp,Dev1)
        self.p2=SubPanel(self.sp,Dev2)
        self.sp.SplitVertically(self.p1,self.p2,200)

def main():
    app=wx.App()
    frame=MainFrame(None,wx.NewId())
    frame.Show()
    app.MainLoop()
    




