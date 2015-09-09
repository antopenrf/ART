import pickle
import thread

import wx
import wx.aui as aui

import EqpTree
import Filing
from MeaCase import *
import MeaDB
from MainGUI_Tree import *
import MeaTree
import RawPanel
import Test
import TestDB


def info():
    info = "ANT Open RF\n" + "ART - Automate RF Testing\n" + "Version: 15.a1 (year 2015, alpha release 1)\n\n" + "Open RF means Open Research Foundation, or Open Raido Frequency.  To contribute open resouce society with my RF knowledge, this RF automation software has been developed and released in its first alpha version.  Currently, only the VNA sweep test is coded with Keysight ENA-series driver.  However, with this software structure being established, other tests and drivers can be quickly added.  If you need any automation test procedure to run your research work, please feel free to contact us at antopenrf@gmail.com."
    wx.MessageBox(info,'About', wx.OK)
                    
class MainFrame(wx.MDIParentFrame):

    load_counts = 0
    save_filename = None
    
    def __init__(self, parent, id=-1, title='ART',pos=(30,30), size=(1000, 800),style=wx.DEFAULT_FRAME_STYLE):#|wx.MAXIMIZE):
        wx.MDIParentFrame.__init__(self, parent, id, title, pos, size, style)
        self._mgr = aui.AuiManager(self)

        # create main frame icon
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("main.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
      
        # create the image list
        self.imagelist=wx.ImageList(16,16)     
        self.imagelist.icon_test=self.imagelist.Add(wx.Bitmap('icon_testing.bmp',wx.BITMAP_TYPE_ANY))
        self.imagelist.icon_mea=self.imagelist.Add(wx.Bitmap('icon_mea.bmp',wx.BITMAP_TYPE_ANY))
        self.imagelist.icon1=self.imagelist.Add(wx.Bitmap('icon_folder.bmp',wx.BITMAP_TYPE_ANY))
        self.imagelist.icon2=self.imagelist.Add(wx.Bitmap('icon_folderopen.bmp',wx.BITMAP_TYPE_ANY))        


        # create the project tree for the upper pane.
        self.projtree=CrtTree(self,'PROJECT')

        # create the test queue list for the lower pane.
        self.queue_flag_lock=0     # flag=1 to lock the queue
        self.queue_flag_greenOn=0  # flag=1 to run test queue continuously without out prompt windown popping out
        self.testlist=wx.ListCtrl(self,-1,style=wx.LC_REPORT)
        self.Set_Testlist()
        
        # add the panes to the manager
        self.projpane1=self._mgr.AddPane(self.projtree, wx.aui.AuiPaneInfo().Left().MinSize((200,-1)).Name('Project').Caption('Project Management').PaneBorder(False))
        self.testqueue=self._mgr.AddPane(self.testlist, wx.aui.AuiPaneInfo().Bottom().MinSize((-1,200)).Name('Queue').Caption('Test Queue (Unlocked) - 0 untested items'))


        # create status bar
        self.statusbar=self.CreateStatusBar()

        # count the number of Mea Panels
        self.count=0
     
        # create menu bar
        menubar=self.CrtMenuBar()
        self.SetMenuBar(menubar)
        self.menu_mea.AppendSeparator()
        self.unlock=self.menu_mea.AppendRadioItem(-1,"Test Queue Unlocked")
        self.lock=self.menu_mea.AppendRadioItem(-1,"Test Queue Locked")
        self.menu_mea.AppendSeparator()
        self.greenlightoff=self.menu_mea.AppendRadioItem(-1,"Green Light OFF")
        self.greenlighton=self.menu_mea.AppendRadioItem(-1,"Green Light ON")
        self.Bind(wx.EVT_MENU,self.OnQueueCheck,self.unlock)
        self.Bind(wx.EVT_MENU,self.OnQueueCheck,self.lock)
        self.Bind(wx.EVT_MENU,self.OnGreenCheck,self.greenlighton)
        self.Bind(wx.EVT_MENU,self.OnGreenCheck,self.greenlightoff)        

        # tell the manager to 'commit' all the changes just made
        self._mgr.GetArtProvider().SetColour(wx.aui.AUI_DOCKART_BORDER_COLOUR,'gray')
        self._mgr.GetPane(self.testlist).Show()
        self._mgr.Update()

    def Set_Testlist(self):
        self.testlist.InsertColumn(0,'no.')
        self.testlist.InsertColumn(1,'title')        
        self.testlist.InsertColumn(2,'test case')
        self.testlist.InsertColumn(3,'comments')
        self.testlist.InsertColumn(4,'test start time')
        self.testlist.InsertColumn(5,'test stop time')
        self.testlist.InsertColumn(6,'total test time')
        self.testlist.InsertColumn(7,'operator name')
        self.testlist.InsertColumn(8,'measurement title')            
        self.testlist.SetColumnWidth(0,40)
        self.testlist.SetColumnWidth(1,100)
        self.testlist.SetColumnWidth(2,80)
        self.testlist.SetColumnWidth(3,300)
        self.testlist.SetColumnWidth(4,200)
        self.testlist.SetColumnWidth(5,200)
        self.testlist.SetColumnWidth(6,200)
        self.testlist.SetColumnWidth(7,200)
        self.testlist.SetColumnWidth(8,200)          
        self.testlist.AssignImageList(self.imagelist,wx.IMAGE_LIST_SMALL)

    def QueueLock(self):
        self.queue_flag_lock=1
        self.lock.Check(True)
        self._mgr.GetPane(self.testlist).Caption('Test Queue (Locked)'+' - '+str(TestDB.TestItemNo)+' untested items')
        self._mgr.Update()        

    def QueueUnlock(self):   
        self.queue_flag_lock=0
        self.unlock.Check(True)
        self._mgr.GetPane(self.testlist).Caption('Test Queue (Unlocked)'+' - '+str(TestDB.TestItemNo)+' untested items')
        self._mgr.Update()

    def OnGreenLightOff(self):
        self.queue_flag_greenOn=0
        self.greenlightoff.Check(True)
        self._mgr.GetArtProvider().SetColour(wx.aui.AUI_DOCKART_BORDER_COLOUR,'gray')        
        self._mgr.Update()
        print self.queue_flag_greenOn
        
    def OnGreenLightOn(self):   
        self.queue_flag_greenOn=1
        self.greenlighton.Check(True)
        self._mgr.GetArtProvider().SetColour(wx.aui.AUI_DOCKART_BORDER_COLOUR,'green')         
        self._mgr.Update()

    # create menu bar handlers #  
    def OnQueueCheck(self,event):
        if self.unlock.IsChecked():
            self.QueueUnlock()
        else:
            self.QueueLock()

    def OnGreenCheck(self,event):
        if self.greenlightoff.IsChecked():
            self.OnGreenLightOff()
        else:
            self.OnGreenLightOn()
            
    def OnNewProj(self, event):
        pass

    def OnCloseProj(self, event):
        code=wx.MessageBox('Close all the projects?','Notice',wx.YES_NO)
        if code == wx.YES:
            self.CloseProj()
        
    def CloseProj(self):
        while MeaDB.MeaDBList != []:
            db = MeaDB.MeaDBList.pop()
            db.meaframe.Destroy()
            self.projtree.Delete(db.treeID)
        MeaDB.mea_tagid = 0
        MeaDB.MeaDBIndex = []

    def OnSaveProj(self, event):
        self.SaveProj()

    def OnCloseAll(self, event):
        if MeaDB.MeaDBList != []:        
            code=wx.MessageBox('Save existing project before close?','Notice',wx.YES_NO)
            if code == wx.YES:
                self.SaveProj()
                self.Close()
            else:
                self.Close()
        else:
            self.Close()
        
    def SaveProj(self):
        dialog=wx.FileDialog(self, "Enter filename to save:", os.path.join(os.getcwd(), 'projects'),"","*.*", wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath()
            if file_path[-3:].lower() != 'prj':
                file_path = file_path + ".prj"
            pickle_file = file(file_path, "wb")
            datadb = pickle.dump(Filing.SavedProj(MeaDB.MeaDBList), pickle_file)
            pickle_file.close()

    def OnLoadProj(self, event):
        if MeaDB.MeaDBList != []:        
            code=wx.MessageBox('Save existing project before load project?','Notice',wx.YES_NO)
            if code == wx.YES:
                self.SaveProj()
                self.CloseProj()
            else:
                self.CloseProj()
                
        dialog=wx.FileDialog(self, "Select project to load:", os.path.join(os.getcwd(), 'projects'),"","*.*", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath()
            filed_pickle = file(file_path, "rb")
            saved_project = pickle.load(filed_pickle)
            filed_pickle.close()
            Filing.LoadProject(self, saved_project)

    def OnLoadData(self, event):
        dialog=wx.FileDialog(self, "Select the data file to import:", os.path.join(os.getcwd(), 'rawdata'),"","*.*", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            TestDB.test_tagid += 1
            file_path = dialog.GetPath()
            filed_pickle = file(file_path, "rb")
            datadb = pickle.load(filed_pickle)
            filed_pickle.close()
            meadb = MeadbGenerator(None, datadb.meatype, datadb.meaID, None, datadb.testname)
            testdb = TestdbGenerator(None, meadb, None, mode = 'load')
            testdb.meadb.iPara = datadb.iPara
            testdb.meadb.iEqpPara = datadb.iEqpPara
            testdb.filename = file_path.split("\\")[-1]
            testdb.meadb.meaname = "loaded: " + str(TestDB.test_tagid) + datadb.testname
            testdb.test_tagid = TestDB.test_tagid
            testdb.comments = datadb.comments
            testdb.operatorname = datadb.operatorname
            testdb.testname = datadb.testname
            treeID = self.projtree.AddDataItem(testdb.meadb.meaname)
            self.projtree.SetItemTextColour(treeID,c_lightblue2)
            testdb.meadb.treeID = treeID
            testdb.treeID = treeID
            testdb.rawdata = datadb.data
            meaframe = RawPanel.RawPanel(self, testdb.meadb.meaname, testdb)
            testdb.meadb.meaframe = meaframe
            DataStorage[TestDB.test_tagid] = testdb

    def AddEquip(self,event):
        EqpTree.EqpTreeFrame(self)

    def AddMea(self,event):
        MeaTree.MeaTreeFrame(self)

    def RunQueue(self,event):
        if TestDB.TestItemNo==0:
            code=wx.MessageBox('No items are in the test queue.','Notice',wx.CANCEL)
        if TestDB.TestItemNo>0 and not self.queue_flag_lock:
            testdb=TestDB.TestQueue[0]
            if not self.queue_flag_greenOn:
                code=wx.MessageBox('Start running the test queue one by one.','Notice',wx.YES_NO)
            else:
                code=wx.MessageBox('Start running the test queue continuously without prompt window interruption.','Notice',wx.YES_NO)
            if code == wx.YES:
                eval('Test.test'+str(testdb.meadb.meaID)+'.StartTest(testdb.testinstance,testdb)')
        elif TestDB.TestItemNo>0 and self.queue_flag_lock:
            code=wx.MessageBox('Test queue is locked.\nUnlock the queue before testing.','Notice',wx.CANCEL)
        else:
            pass

    def ClearQueue(self,event):
        self.testlist.DeleteAllItems()
        TestDB.TestQueue = {}
        TestDB.TestItemNo = 0

    def ShowTree(self,event):
        self._mgr.GetPane(self.projtree).Show()
        self._mgr.Update()

    def HideTree(self,event):
        self._mgr.GetPane(self.projtree).Hide()
        self._mgr.Update()

    def ShowQueue(self,event):
        self._mgr.GetPane(self.testlist).Show()
        self._mgr.Update()

    def HideQueue(self,event):
        self._mgr.GetPane(self.testlist).Hide()
        self._mgr.Update()        
                
    def About(self,event):  ##### Development Info.
        info()
        
    # create menu bar - begin #  
    def menudata(self):    
        New = ('&New','New a project.', self.OnNewProj)
        Save = ('&Save project','Save a project.', self.OnSaveProj)
        Load_Project = ('&Load project','Load a project.', self.OnLoadProj)
        Load_Data = ('&Load data', 'Load data.', self.OnLoadData)
        Close_Project = ('&Close project', 'Close a project.', self.OnCloseProj)
        Close=('&Close', 'Close.', self.OnCloseAll)
        
        AddEquip=('&Configure','Add in equipments and assign GPIB addresses.', self.AddEquip)
        ShowProj=('&Show Project Tree', 'Show the Project Management Tree.', self.ShowTree)
        HideProj=('&Hide Project Tree', 'Hide the Project MAnagement Tree.', self.HideTree)        
        ShowQueue=('&Show Test Queue', 'Show the Test Queue panel.', self.ShowQueue)
        HideQueue=('&Hide Test Queue', 'Hide the Test Queue panel.', self.HideQueue)        
        AddMea=('&Add Measurement', 'Generate new tests.', self.AddMea)
        RunQueue=('&Run Test Queue', 'Start testing all the items in the test queue.', self.RunQueue)
        ResetTestID=('&Reset Test No', 'Reset test tag ID back to 1', self.ResetTestID)
        En_AutoApply=('&Auto Apply Correction', 'Automatically Apply Correction Data', self.En_AutoApply)
        Dis_AutoApply=('&Disable Auto Apply', 'Ask before Applying Correction Data', self.Dis_AutoApply)        
        ClearQueue=('&Clear Test Queue', 'Clear all the items in the test queue.', self.ClearQueue)        
        About=('&About', 'Automation of RF Testing - ANT Open RF', self.About)
        
        menulist=[('&File'       ,(New, Save, Load_Project, Load_Data, Close_Project, Close)            ),
                  ('&Panels'     ,(ShowProj,HideProj,ShowQueue,HideQueue)         ),
                  ('&Equipment'  ,(AddEquip,)                   ),
                  ('&Measurement',(AddMea, RunQueue, ClearQueue, ResetTestID, En_AutoApply, Dis_AutoApply)  ),
                  ('&Help'       ,(About,)                      )]
        return menulist

    def En_AutoApply(self, event):
        Test.test.AutoApply = True

    def Dis_AutoApply(self, event):
        Test.test.AutoApply = False
        
    def ResetTestID(self, event):
        TestDB.test_tagid = 0

    def CrtMenuBar(self):  
        menubar=wx.MenuBar()
        for each in self.menudata():
            items=each[1]
            label=each[0]
            menu=self.CrtMenu(items)
            menubar.Append(menu,label)
            if label=='&Measurement':
                self.menu_mea=menu
        return menubar
    
    def CrtMenu(self,MenuItem):
        menu=wx.Menu()
        for each in MenuItem:
            label=each[0]
            helptext=each[1]
            handler=each[2]
            item=menu.Append(wx.NewId(),label,helptext)
            self.Bind(wx.EVT_MENU,handler,item)      
        return menu
    # create menu bar - end #  


# Starting the mainloop #
if __name__ == '__main__':
    app = wx.App()

    frame = MainFrame(None)
    frame.GPIB_token=thread.allocate_lock()
    frame.Show()
    
    app.MainLoop()
