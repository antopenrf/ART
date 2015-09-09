import wx
from MeaTree import *
import wx.aui as aui


class MeaPanel(aui.AuiMDIChildFrame):
    def __init__(self,parent,title):
        aui.AuiMDIChildFrame.__init__(self,parent,-1,title)
        

        
class CrtMea212(MeaPanel):
    def __init__(self,parent,meatype,meanumber):
        parent.count+=1
        MeaPanel.__init__(self,parent,title=meatype+': '+str(parent.count))
        
        



        
