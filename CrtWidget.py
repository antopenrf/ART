import wx
##TreeCtrl = wx.TreeCtrl  
import wx.lib.agw.customtreectrl as TreeCtrl
TreeCtrl=TreeCtrl.CustomTreeCtrl
from admin import *
from EqpLibrary import *



def CrtBoldText(parent,label,fontsize,color):
    text=wx.StaticText(parent,-1,label)
    text.SetForegroundColour(color) # set text color
    font = wx.Font(fontsize, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    text.SetFont(font)
    return text


class CrtTree(TreeCtrl):
    def __init__(self,panel,rootlabel,treelist,icon1=None,icon2=None):
        TreeCtrl.__init__(self,panel)
        root=self.AddRoot(rootlabel)
        self.GrowTree(root,treelist,icon1,icon2)
        self.ExpandAll()
        
    def GrowTree(self,parentItem,Items,icon1,icon2):
        for each in Items:
            if type(each)==str:
                newitem=self.AppendItem(parentItem,each)
                if icon1 != None or icon2 != None:
                    self.SetItemImage(newitem,icon1,wx.TreeItemIcon_Normal)
                    self.SetItemImage(newitem,icon2,wx.TreeItemIcon_Selected)                
            else:
                newParent=self.AppendItem(parentItem,each[0])
                newItems=each[1]
                self.GrowTree(newParent,newItems,icon1,icon2)        
        
        
class CrtTreeFrame(wx.Frame):
    def __init__(self,parent,frametitle,rootlabel,treelist,img,spdistance,sxy=(800,600),pxy=(150,100)):

        self.parent=parent #This parent refers to the MainGUI frame.
        wx.Frame.__init__(self,parent,id=-1,size=sxy,pos=pxy,title=frametitle
                          ,style=wx.FRAME_FLOAT_ON_PARENT|wx.RESIZE_BORDER|wx.CAPTION|wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.FRAME_TOOL_WINDOW)
        sp=wx.SplitterWindow(self)
        self.panel=wx.Panel(sp)

        #Make the tree.
        il=wx.ImageList(16,16)
        bmp1=wx.Bitmap(img[0],wx.BITMAP_TYPE_ANY)
        bmp2=wx.Bitmap(img[1],wx.BITMAP_TYPE_ANY)                
        self.icon1=il.Add(bmp1)
        self.icon2=il.Add(bmp2)         
        self.tree=CrtTree(sp,rootlabel,treelist,self.icon1,self.icon2)    
        self.tree.AssignImageList(il)
        
        sp.SplitVertically(self.tree,self.panel,spdistance)
     
        # binding event of double click on the tree item
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.OnDClick,self.tree)
        # binding event of double click on the tree item
        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.OnClick,self.tree)        
        self.parent.Enable(False)    #Disable the Main GUI Frame (MGF) as the main tree frame is called out.
 
    def OnClick(self,event):
        pass  #Define a handler to be overriden by its inheritance due to KEY_DOWN.

    def OnDClick(self,event):
        pass  #Define a handler to be overriden by its inheritance due to ITEM_ACTIVATED.
  
    def __del__(self):
        self.parent.Enable(True)


class CrtFrame(wx.Frame):
    def __init__(self,parent,frametitle,sxy=(400,400),pxy=(250,250)):
        self.parent=parent
        wx.Frame.__init__(self,parent,id=-1,size=sxy,pos=pxy,title=frametitle
                          ,style=wx.FRAME_FLOAT_ON_PARENT|wx.RESIZE_BORDER|wx.CAPTION|wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.FRAME_TOOL_WINDOW)
        self.panel=wx.Panel(self,style=wx.SUNKEN_BORDER)
        self.parent.Enable(False)
        
        
    def TextandChoice(self,label,ChoiceList):
        text=wx.StaticText(self.panel,-1,label,size=(-1,-1),style=wx.TE_LEFT)
        newid=wx.NewId()
        choice=wx.Choice(self.panel,id=newid,size=(-1,-1),choices=ChoiceList)
        sizer=wx.GridSizer(rows=1,cols=2,hgap=5,vgap=5)
        sizer.Add(text,0,wx.ALL,5)
        sizer.Add(choice,0,0)
        return text,choice,sizer,newid
    
    def Text(self, label, sxy = (-1, -1), pxy = (10, 10)):
        wx.StaticText(self.panel, -1, label, size = sxy, pos = pxy, style = wx.TE_LEFT)

    def TextCtrl(self, value = '1', sxy = (-1, -1), pxy = (10, 50)):
        textctrl=wx.TextCtrl(self.panel, -1, value, size = sxy, pos = pxy)
        return textctrl

    def OK_Button(self):
        button = wx.Button(self.panel, wx.ID_OK, "OK", pos=(10, 80))
        return button
    
    def TextandCtrl(self,label,value):
        text=wx.StaticText(self.panel,-1,label,size=(-1,-1),style=wx.TE_LEFT)
        textctrl=wx.TextCtrl(self.panel,-1,value,size=(160,25))
        sizer=wx.GridSizer(rows=1,cols=2,hgap=10,vgap=10)
        sizer.Add(text,0,wx.ALL,5)
        sizer.Add(textctrl,0,0)
        return text,textctrl,sizer     
        
    def __del__(self):
        self.parent.Enable(True)


class CheckingDialog(wx.Dialog):
    def __init__(self,mainGUIframe):
        mainGUIframe.Enable(False)        
        pixels = tuple (mainGUIframe.GetClientSize())        
        wx.Dialog.__init__(self,None,id=-1,size=(350,180),pos=(pixels[0]/2-175,pixels[1]/2-90),title='Updating',style=wx.FRAME_TOOL_WINDOW)
        self.mainGUIframe=mainGUIframe
        self.SetBackgroundColour(c_lightblue)
        wx.StaticText(self,-1,'Verification of Test Parameters',pos=(20,10),style=wx.TE_LEFT)
        wx.StaticLine(self,-1,pos=(10,30),size=(330,2),style=wx.LI_HORIZONTAL)        
        self.status=wx.StaticText(self,-1,'Verifying .... ',pos=(20,50),style=wx.TE_LEFT)
        self.text=wx.StaticText(self,-1,'',pos=(20,90),style=wx.TE_LEFT)
        self.okButton=wx.Button(self,wx.ID_OK,"OK",pos=(130,140))
        self.okButton.Hide()        
        self.cancelButton=wx.Button(self,wx.ID_CANCEL,"Cancel",pos=(240,140))
        self.cancelButton.Hide()     
        self.Bind(wx.EVT_BUTTON,self.DialogClose,self.cancelButton)
        self.Bind(wx.EVT_BUTTON,self.Continue,self.okButton)        
        self.Show()
                

    def Updating(self,text):
        self.text.SetLabel(text)
        
    def Uncompleted(self,text):
        self.text.SetLabel(text)
        self.status.SetLabel('Failed!')
        self.cancelButton.Show()

    def DialogClose(self,event):
        self.Destroy()

    def Completed(self,text,dofunction):
        self.text.SetLabel(text)
        self.cancelButton.Show()
        self.okButton.Show()
        self.status.SetLabel('Done!')                           
        self.dofunction=dofunction

    def Continue(self,event):
        self.Destroy()        
        self.dofunction()

    def __del__(self):
        self.mainGUIframe.Enable(True)
        

class PwdCtrl():
    pass


def WarningFrame(message):
    dlg=wx.MessageDialog(None,message,style=wx.OK)
    dlg.ShowModal()



def YesNoBox(text,dofunction,*arg):
    dlg=wx.Dialog(None,-1,'Notice',size=(240,155),pos=(-1,400),style=wx.OK|wx.CANCEL|wx.FRAME_TOOL_WINDOW|wx.CAPTION)
    dlgtext=wx.StaticText(dlg,-1,text,pos=(20,20))
    okButton=wx.Button(dlg,wx.ID_OK,"OK",pos=(15,90))     
    cancelButton=wx.Button(dlg,wx.ID_CANCEL,"Cancel",pos=(130,90))    
    code=dlg.ShowModal()
    if code==wx.ID_OK:
        dofunction(*arg)
    else:
        pass
    dlg.Destroy()    

def OkBox(message):
    dlg=wx.MessageBox(message,'Notice',wx.OK)


def ChoiceExclusion(window,selectedID,idlist,exlist):
    idlist.remove(selectedID)
    anotherid=idlist[0]
    widget=window.FindWindowById(selectedID)    
    anotherwidget=window.FindWindowById(anotherid)
    selectedchoice=widget.GetStringSelection()
    exlist.remove(selectedchoice)
    anotherchoice=exlist[0]
    anotherwidget.SetStringSelection(anotherchoice)
    return anotherid



