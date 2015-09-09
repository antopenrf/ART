
import wx.lib.agw.customtreectrl as TreeCtrl
TreeCtrl=TreeCtrl.CustomTreeCtrl
import wx

from admin import *
from CrtWidget import *
import Filing
from MeaDB import *
import RawPanel
from Test import test
from TestDB import *


ProjectList=[   'Note', 'Frequency' , 'Measurement' , 'Data' , 'Analysis' , 'System' ]

class CrtTree(TreeCtrl):
    LeafSelected=None  ### This will be the selected MeaDB object.
    def __init__(self,parent,rootlabel,treelist=ProjectList,icon1=None,icon2=None):
        TreeCtrl.__init__(self,parent,agwStyle=wx.TR_HIDE_ROOT)
        self.parent=parent
        self.projroot=self.AddRoot(rootlabel)
        self.projitem=[]
        font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.SetItemFont(self.projroot,font)
        self.SetBackgroundColour((255,255,255))       
        self.AssignImageList(self.parent.imagelist)         
        self.GrowTree(self.projroot,treelist,self.parent.imagelist.icon1)        
        
        ## Bind event of double click on the tree item.
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.OnDClick,self)
        # create popmenu for the tree
        self.mea_menu=wx.Menu()
        self.data_menu=wx.Menu()
        ## Bind popmenu events for Measurement leaf.
        for each in ['Open','Close','Delete','Spawn']:
            item=self.mea_menu.Append(-1,each)
            parent.Bind(wx.EVT_MENU,self.On_MeaMenu,item)  ## Only the wx.Panel or (wx.Frame) instance can binds menu events.
        ## Bind popmenu events for Data leaf.
        for each in ['Open','Close', 'Export', 'Delete']:
            item=self.data_menu.Append(-1,each)
            parent.Bind(wx.EVT_MENU,self.On_DataMenu,item) ## Only the wx.Panel or (wx.Frame) instance can binds menu events.
        parent.Bind(wx.EVT_TREE_ITEM_MENU,self.On_ClickOutPopMenu)
        
    def On_MeaMenu(self,event):  #Define the actions for the Measurement drop-down menu.
        item=self.mea_menu.FindItemById(event.GetId())
        itemtext=item.GetText()
        meadb = CrtTree.LeafSelected
        def dothis():
            meadb.meaframe.Destroy()
            DBremove(meadb)
            self.RemoveMeaItem(meadb.treeID)

        if itemtext == 'Spawn':
            Spawn_Frame = CrtFrame(self.parent, "Spawn measurement: " + meadb.meaname, sxy = (250, 150), pxy = (300, 300))
            Spawn_Frame.Text("Number of measurements to spawn?")
            ctl = Spawn_Frame.TextCtrl()
            but = Spawn_Frame.OK_Button()
            def spawn_howmany(event):
                nos = ctl.GetValue() ## number of spawn
                if nos.isnumeric():
                    code = wx.MessageBox("Spawn " + nos + " measurement?", 'notice', wx.YES_NO)
                    if code == wx.YES:
                        meadb.meaframe.parent.QueueLock()
                        Spawn_Frame.Destroy()
                        test.run_in_spawn = True ## imported from Test.py
                        test.number_of_spawn = int(nos)
                        meadb.meaframe._Run()
                        
                    else:
                        Spawn_Frame.Destroy()
                else:
                    wx.MessageBox("Entry is not integer!", 'notice', wx.CANCEL)
                    Spawn_Frame.Destroy()
                        
            self.parent.Bind(wx.EVT_BUTTON, spawn_howmany, but)
            Spawn_Frame.Show()

            
        if itemtext == 'Delete':
            if meadb.flag_in_Testing:
                OkBox('Testing is in progress.\nStop the test before deleting this measurement item.')
            elif meadb.testinqueue>0:
                OkBox('There are untested items associated with this measurement.\nClear the untested items before deleting this measurement.')
            else:
                code=wx.MessageBox('Delete this measurement item permenantly?','Notice',wx.YES_NO)
                if code==wx.YES: dothis()

        if itemtext == 'Open':
            meadb.meaframe.Show()
            meadb.meaframe.Activate()
            self.SetItemTextColour(meadb.treeID,c_blue)
            
        if itemtext == 'Close':
            self.SetItemTextColour(meadb.treeID,c_lightblue2)
            meadb.meaframe.Hide()          

    def On_DataMenu(self,event):  #Define the actions for the Data drop-down menu.
        item = self.data_menu.FindItemById(event.GetId())
        itemtext = item.GetText()
        testdb = CrtTree.LeafSelected
        if itemtext == 'Delete':
            code=wx.MessageBox('Delete this data item permenantly?','Notice',wx.YES_NO)
            if code==wx.YES:
                self.RemoveMeaItem(testdb.treeID)
                DataStorage.pop(testdb.test_tagid)

        if itemtext == 'Open':
            testdb.meadb.meaframe.Show()
            testdb.meadb.meaframe.Activate()
            self.SetItemTextColour(testdb.meadb.treeID,c_blue)

        if itemtext == 'Export':
            dialog=wx.FileDialog(self, "Enter filename to Export:", os.path.join(os.getcwd(), 'export'),"","*.dat", wx.SAVE)
            if dialog.ShowModal() == wx.ID_OK:
                data_to_export = testdb.rawdata
                file_path = dialog.GetPath()
                if file_path[-3:].lower() != 'dat':
                    file_path = file_path + ".dat"
                export_file = file(file_path, "w")
                Filing.ExportRaw(testdb.meadb.meaID, export_file, data_to_export)
            
        if itemtext == 'Close':
            self.SetItemTextColour(testdb.meadb.treeID,c_lightblue2)
            testdb.meadb.meaframe.Hide()


    def On_ClickOutPopMenu(self,event):
        totalList=MeaDBList+DataStorage.values()
        mealen=len(MeaDBList)
        n=1
        for each in totalList:
            if event.GetItem()==each.treeID:
                CrtTree.LeafSelected=each
                if n>mealen:
                    self.parent.PopupMenu(self.data_menu)
                    break
                else:
                    self.parent.PopupMenu(self.mea_menu)
                    break
            n+=1

    def OnDClick(self,event):
        for each in MeaDBList:   ## From MeaDB module.
            if event.GetItem()==each.treeID:
                each.meaframe.Show()
                each.meaframe.Activate()
                self.SetItemTextColour(each.treeID,c_blue)                
                break

        for each in DataStorage.values(): ## From TestDB module.
            if event.GetItem()==each.meadb.treeID:
                if not each.rawpanel_exist:
                    meaframe = RawPanel.RawPanel(self.parent, each.meadb.meaname, each)
                    each.meadb.meaframe = meaframe    
                    each.rawpanel_exist = True
                each.meadb.meaframe.Show()
                self.SetItemTextColour(each.meadb.treeID, c_blue)                
                break
        
    def GrowTree(self,parentItem,Items,icon1):
        for each in Items:
            if type(each)==str:
                font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD)
                newitem=self.AppendItem(parentItem,each)
                self.projitem.append(newitem)
                self.SetItemFont(newitem,font)
                self.SetItemTextColour(newitem,c_blue)
                if icon1 != None or icon2 != None:
                    self.SetItemImage(newitem,icon1,wx.TreeItemIcon_Normal)
            else:
                newParent=self.AppendItem(parentItem,each[0])
                newItems=each[1]
                self.GrowTree(newParent,newItems,icon1,icon2)     

    def AddMeaItem(self,meaname):
        ItemID=self.AppendItem(self.projitem[2], meaname)
        self.SetItemTextColour(ItemID,c_blue)
        self.SetItemImage(ItemID, self.parent.imagelist.icon_mea, wx.TreeItemIcon_Normal)      
        self.ExpandAll()        
        return ItemID

    def AddDataItem(self,testname):
        ItemID=self.AppendItem(self.projitem[3], testname)
        self.SetItemTextColour(ItemID,c_blue)
        self.SetItemImage(ItemID, self.parent.imagelist.icon_test, wx.TreeItemIcon_Normal)      
        self.ExpandAll()        
        return ItemID    

    def RemoveMeaItem(self,meaitem):     
        self.Delete(meaitem)         
        self.ExpandAll()

    def RemoveDataItem(self,testitem):     
        self.Delete(testitem)         
        self.ExpandAll()
            
