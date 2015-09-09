#2012 Aug 3
#plot examples

##import pylab
##pylab.figure()
##pylab.plot(range(3))
##pylab.show()

# This example is equivalent with pyplot

##import matplotlib.pyplot
##matplotlib.pyplot.figure()
##matplotlib.pyplot.plot(range(3))
##matplotlib.pyplot.show()

# Then this example can be created directly into the heart of matplotlib.figure module
# Not completed yet, still gets frozen
##import matplotlib
##import matplotlib.figure
##import matplotlib.pyplot
##
##fig=matplotlib.pyplot.figure()
##line1 = matplotlib.lines.Line2D([0,1],[0,1], transform=fig.transFigure, figure=fig, color="r")
##line2 = matplotlib.lines.Line2D([0,1],[1,0], transform=fig.transFigure, figure=fig, color="g")
##fig.lines.extend([line1, line2])
##fig.show()


import MeaPlot
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_wxagg
Canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg 

import wx
import matplotlib.backends.backend_wx
NavTool = matplotlib.backends.backend_wx.NavigationToolbar2Wx
import math
pi = math.pi
sin = math.sin

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,size=(500,500))
        sp=wx.SplitterWindow(self)
        p1=wx.Panel(sp)
        p2=MeaPlot.Figure2D(sp)
        sp.SplitVertically(p1,p2)
        
class MainPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,-1)

        self.figure=matplotlib.figure.Figure()

        self.axes=self.figure.add_subplot(111,polar=True)
 
        self.d=range(0,360,1)
        self.t=map((lambda x: x/180.0*pi),self.d)
        self.r=map(sin,self.t)
        self.axes.plot(self.t,self.r)        
        self.canvas=Canvas(self,-1,self.figure)

        self.toolbar=NavTool(self.canvas) 
        self.toolbar.Realize()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 0
                  )
        sizer.Add(self.toolbar, 1 , wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_IDLE,self._OnIdle)
        self.Bind(wx.EVT_SIZE,self._OnSize)
        
        self._SetSize()

        self._resizeflag = False
      
 
    def _OnIdle(self,event):
        if self._resizeflag == True:
            self._resizeflag = False
            self._SetSize()
            
    def _OnSize(self,event):

        self._resizeflag = True

    def _SetSize(self):
        
        fw, fh = self.canvas.GetSizeTuple()
        self.toolbar.SetSize(wx.Size(fw, fh))
        self.toolbar.update()
        
        pixels = tuple (self.GetClientSize())
        self.SetSize(pixels)
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches(float( pixels[0] )/self.figure.get_dpi(),
                                     float( pixels[1] )/self.figure.get_dpi() )
        
##        but=wx.Button(self.panel,-1)
##        panel.Bind(wx.EVT_BUTTON,self.size,but)
##
##    def size(self,event):
##        print self.GetClientSize()
##        print self.panel.GetClientSize()            
                
app=wx.App()
frame=MainFrame()
frame.Show()

app.MainLoop()
