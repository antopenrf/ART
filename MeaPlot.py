import wx
from admin import *
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_wxagg
from matplotlib.lines import Line2D
Canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg 



        
class Figure2D(wx.Panel):
    def __init__(self,parent, notraces = 1):
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
        self.traces = []

        self.notraces = notraces
        self.reset_notraces(notraces)

        self.canvas.draw()

        

    def reset_notraces(self, notraces):
        self.traces = []
        for each in range(notraces):
            added_line = Line2D([],[])
            self.traces.append(added_line)
            self.axes.add_line(added_line)
        self.canvas.draw()


    def set_notraces(self, notraces):
        self.notraces = notraces
        
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


    def _set_min_max(self, data):
        minimum = mininlist(data)
        if minimum > 0:
            minimum = minimum*0.9
        else:
            minimum = minimum*1.1
        maximum = maxinlist(data)
        if maximum > 0:
            maximum = maximum*1.1
        else:
            maximum = maximum*0.9
        return minimum, maximum
    
    def drawgraph(self, xdata, *ydata):
        x_min = mininlist(xdata)
        x_max = maxinlist(xdata)

        if x_min == x_max:
            x_min, x_max = self._set_min_max(xdata)

        all_ydata = []
        for k, each in enumerate(ydata):
            all_ydata += each

        y_min, y_max = self._set_min_max(all_ydata)        

        self.axes.set_xlim(x_min, x_max)
        self.axes.set_ylim(y_min, y_max)

        for k, each in enumerate(self.traces):
            each.set_xdata(xdata)
            each.set_ydata(ydata[k])

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
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches(float( pixels[0] )/self.figure.get_dpi(),
                                     float( pixels[1] )/self.figure.get_dpi() )
        
if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, 'Plot')

    plotter = Figure2D(frame, notraces = 1)
    plotter.reset_notraces(2)
    plotter.drawgraph(range(10), [9,8,7,6,5,4,3,2,1,0], range(10))
    frame.Show()
    app.MainLoop()
    
