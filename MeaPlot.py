import wx
from admin import *
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_wxagg
Canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg 



        
class Figure2D(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,-1,style=wx.SUNKEN_BORDER)

        self.figure=matplotlib.figure.Figure(facecolor='white' )
        self.axes=self.figure.add_subplot(111,polar=False)
        self.canvas=Canvas(self,-1,self.figure)     
        
        self.Bind(wx.EVT_IDLE,self._OnIdle)
        self.Bind(wx.EVT_SIZE,self._OnSize)
        
        self._resizeflag = False        
        self._SetSize()

        self.xdata=[]
        self.ydata=[]
        self.trace,=self.axes.plot([],[])        
        self.canvas.draw()

    def drawlabels(self,label_x,label_y):
        self.axes.set_xlabel(label_x,labelpad=30)
        self.axes.set_ylabel(label_y,labelpad=30)        

    def drawtitle(self, title):
        self.axes.set_title(title)

    def drawxlimit(self,alist):
        if len(alist)==1:
            alist=[int(alist[0]*1.1),int(alist[0]*0.9)]
        self.axes.set_xlim(mininlist(alist),maxinlist(alist))        
        self.canvas.draw()
        
    def drawgraph(self,xdata,ydata):
        minimum = mininlist(ydata)
        if minimum > 0:
            minimum = minimum*0.9
        else:
            minimum = minimum*1.1
        maximum = maxinlist(ydata)
        if maximum > 0:
            maximum = maximum*1.1
        else:
            maximum = maximum*0.9
        self.axes.set_xlim(mininlist(xdata), maxinlist(xdata))
        self.axes.set_ylim(minimum, maximum)
        self.trace.set_xdata(xdata)
        self.trace.set_ydata(ydata)
        self.canvas.draw()
        
    def _OnIdle(self,event):
        try:
            if self._resizeflag == True:
                self._resizeflag = False
                self._SetSize()
        except TypeError:
            pass
            
    def _OnSize(self,event):
        self._resizeflag = True

    def _SetSize(self):
        pixels = tuple (self.GetClientSize())
##        self.SetSize(pixels)
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches(float( pixels[0] )/self.figure.get_dpi(),
                                     float( pixels[1] )/self.figure.get_dpi() )
        
