import wx
import MeaTree

class x:
    def __init__(self,value):
        self.value=value

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1)
        #self.panel=wx.Panel(self)

        self.tree=wx.TreeCtrl(self)
        root=self.tree.AddRoot('Measurements')
        self.GrowTree(root,MeaTree.MeaList)
        
    def GrowTree(self,parentItem,Items):
        for each in Items:
            if type(each)==str:
                self.tree.AppendItem(parentItem,each)
            else:
                newParent=self.tree.AppendItem(parentItem,each[0])
                newItems=each[1]
                self.GrowTree(newParent,newItems)

        
##        c1=self.tree.AppendItem(root,'yulung')

        
##        self.tree.AppendItem(c1,'y1')
##        self.tree.AppendItem(c1,'y2')
##        self.tree.AppendItem(c1,'y3')
##        c2=self.tree.AppendItem(root,'kimmy')
##

##        a=x(1)
##        b=x(2)
##
##        self.tree.SetItemPyData(c1,a)
##        self.tree.SetItemPyData(c2,b)
##
##        print self.tree.GetItemPyData(c1)
##        temp=self.tree.GetItemPyData(c1)
##        print temp.value
##        
##        print self.tree.GetItemPyData(c2)
##        temp=self.tree.GetItemPyData(c2)
##        print temp.value

        
app=wx.App()
frame=MainFrame()
frame.Show()
app.MainLoop()
