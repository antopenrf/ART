import os

import wx
import wx.grid  
import wx.lib.masked.numctrl
NumCtrl=wx.lib.masked.numctrl.NumCtrl

from admin import *
from CrtWidget import *
import MeaPlot



#MeaPanel is the superclass that will be inherited by all children(which are named after meaID) measurement panels.
class RawPanel(wx.MDIChildFrame):
    sp1pos=900

    def __init__(self, parent, title, testdb):
        ## This parent is the MainGUI frame.
        ## 'self' referes to the MeaPanel Frame itself; parent here refers to the Main GUI frame.
        wx.MDIChildFrame.__init__(self, parent, -1, title, size=(750,750))

        self.parent = parent
        self.testdb = testdb
        
        self._LayoutMain()
        self._LayoutPlotter()
        self._Plotter_Graph()
        self._Layout_PanelS()
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("raw.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        ## Bind the EVT_CLOSE event.
        self.Bind(wx.EVT_CLOSE, self.Close)

        self.Hide()

    def _Layout_PanelS(self):
        x1, y1 = 5, 5
        delta_x = 160
        delta_y = 30

        tags_list = ("File Name:", "Operator Name:", "Measurement Type:")
        info_list = (self.testdb.filename, self.testdb.operatorname, self.testdb.meadb.meatype)
        for k, each in enumerate( tags_list):
            wx.StaticText(self.panelS, -1, each, pos = (x1, y1 + delta_y*k), size = (-1, -1), style=wx.TE_LEFT)
            wx.StaticText(self.panelS, -1, info_list[k], pos = (x1 + delta_x, y1 + delta_y*k), size = (-1, -1), style=wx.TE_LEFT)

        wx.StaticText(self.panelS, -1, "Information:", pos = (x1, y1 + delta_y*len(tags_list)), size = (-1, -1), style=wx.TE_LEFT)
        ctrltext = wx.TextCtrl(self.panelS, -1, pos = (x1, delta_y*(len(tags_list) + 1) ), size = (500, 300), style=wx.TE_MULTILINE)

        meaID = str(self.testdb.meadb.meaID)
        mea_info = self.testdb.meadb.iPara[meaID]  ## This is the measurment parameter dict.
        for each in mea_info:
            if each == 'para':
                for k, each_para in enumerate(mea_info['para']):
                    infotext = each_para + ":" + str(mea_info['value'][k])
                    ctrltext.AppendText(infotext + '\n')
            elif each == 'value':
                pass
            else:
                infotext = each + ": " + str(mea_info[each])
                ctrltext.AppendText(infotext + '\n')
        ctrltext.AppendText("\nComments:\n")
        ctrltext.AppendText(self.testdb.comments)

        
    def _Plotter_Graph(self):
        self.plotter.drawgraph(self.testdb.rawdata['x'], self.testdb.rawdata['y'])
        self.plotter.drawtitle(self.testdb.testname)
            

    def _LayoutPlotter(self):
        xdimension=self.testdb.meadb.iPara[str(self.testdb.meadb.meaID)]['axes'][1]
        ydimension=self.testdb.meadb.iPara[str(self.testdb.meadb.meaID)]['axes'][0]
        self.plotter.drawlabels(xdimension,ydimension)
                                

    def _LayoutMain(self):
        """Private method: main raw data panel layout."""
        ## Set the splitter window
        self.sp1 = wx.SplitterWindow(self)
        self.panelS = wx.Panel(self.sp1, style=wx.SUNKEN_BORDER)  ## wx.Panel addes onto the scroll window.
        self.panelS.SetBackgroundColour(c_silver)
        self.plotter = MeaPlot.Figure2D(self.sp1)     ## The upper part: Matplotlib figure instance
        self.sp1.SplitHorizontally(self.plotter, self.panelS)
        self._SetSplitter(self.sp1, RawPanel.sp1pos)


        ## Bind a method to make the sash unmovable
##        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED,self._OnSashChanged1,self.sp1)


    def Close(self, event):
        ## The meaDB instance will be removed from the database list.  Also remove from the project tree.
        self.Hide()


    def _LayoutLower(self):
        """Private method: lower part for testing parameter display."""
        ## This will be overwritten by inheriting class.
        pass
        

    def _SetSplitter(self, splitter, pos, minpos=50):
        splitter.SetMinimumPaneSize(minpos)
        splitter.SetSashPosition(pos, redraw=True)

        
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
    
    def TextandTextCtrl(self, relf, label, sx=300, sy=-1, textstyle=wx.TE_LEFT):
        text=wx.StaticText(relf,-1,label,size=(sx,-1),style=wx.TE_LEFT)
        font = wx.Font(gfontsize, gfont_para, wx.NORMAL,wx.NORMAL)
        text.SetFont(font)        
        tctrl=wx.TextCtrl(relf,-1,size=(sx,sy),style=textstyle)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text,0,wx.ALL,border=2)
        sizer.Add(tctrl,0,wx.ALL,border=2)
        return text,tctrl,sizer
  
    def AdvTextChoice(self, telf, label, pxy, ChoiceList):
        text = wx.StaticText(telf, -1, label, pos=pxy, style=wx.TE_LEFT)
        font = wx.Font(gfontsize, gfont_para, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)
        newid = wx.NewId()
        choice = wx.Choice(telf, id=newid, pos=(pxy[0]+170, pxy[1]-5), choices=ChoiceList)
        return text, choice, newid

