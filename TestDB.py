import copy
import os
import pickle

import wx

from admin import *
import DataDB
import RawPanel
import Test

dir_rawdata="rawdata"

TestQueue={}
DataStorage={}
TestItemNo=0  ## Indicate the number of untested items in the queue.
test_tagid=0  ## Indicate the serial number of all generated test items.
    

        
def TestDBremove(para=1):
    global TestItemNo
    completed_testdb = TestQueue.pop(0)
    completed_testdb.meadb.testinqueue -= 1
    queue_flag_lock = completed_testdb.meadb.meaframe.parent.queue_flag_lock    
    testlist = completed_testdb.meadb.meaframe.testlist #This links to the test queue list (instance of self.testlist of MainGUI frame.)
    TestItemNo -= 1 

    ## Move the testdb(the one on the top of the queue) to the project tree from the test queue.
    testlist.DeleteAllItems()
    DataStorage[completed_testdb.test_tagid]=completed_testdb
    meadb = copy.copy(completed_testdb.meadb)
    completed_testdb.meadb = meadb
    name = str(completed_testdb.test_tagid) +'. '+ completed_testdb.testname
    meadb.meaname = name
    completed_testdb.treeID = meadb.meaframe.projtree.AddDataItem(name)  ## Here is to add onto the tree.
    meadb.meaframe.projtree.SetItemTextColour(completed_testdb.treeID, c_lightblue2)
    meadb.treeID = completed_testdb.treeID

    mainframe_mgr = completed_testdb.meadb.meaframe.parent._mgr
    if queue_flag_lock:
        mainframe_mgr.GetPane(testlist).Caption('Test Queue (Locked)'+' - '+str(TestItemNo)+' untested items')
        mainframe_mgr.Update()
    else:
        mainframe_mgr.GetPane(testlist).Caption('Test Queue (Unlocked)'+' - '+str(TestItemNo)+' untested items')
        mainframe_mgr.Update()
    ## Referesh the list after testing.    
    for each in range(len(TestQueue)):
        TestQueue[each]=TestQueue.pop(each+1)
        meaID=TestQueue[each].meadb.meaID
        testlist.InsertImageStringItem(each,str(each+1),completed_testdb.meadb.meaframe.imagelist.icon_test)
        testlist.SetStringItem(each,1,TestQueue[each].testname)
        testlist.SetStringItem(each,2,' '+str(meaID))
        testlist.SetStringItem(each,3,TestQueue[each].comments)
        testlist.SetStringItem(each,7,TestQueue[each].operatorname)
        testlist.SetStringItem(each,8,TestQueue[each].meatitle)
    
    ## Write the testdb into the pickled file.
    tempfile = open( os.path.join(os.getcwd(), dir_rawdata, completed_testdb.filename + ".pkl"), 'wb' )
    pickle.dump(DataDB.DatadbGenerator(completed_testdb),tempfile)        
    tempfile.close()

 
def TestDBadd(testdb):
    global TestItemNo
    global test_tagid
    queue_flag_lock=testdb.meadb.meaframe.parent.queue_flag_lock
    testdb.meadb.testinqueue+=1
    test_tagid+=1
    testlist=testdb.meadb.meaframe.testlist
    meaID=testdb.meadb.meaID
    TestQueue[TestItemNo]=testdb
    testdb.test_tagid=test_tagid
    testlist.InsertImageStringItem(TestItemNo,str(TestItemNo+1),testdb.meadb.meaframe.imagelist.icon_test)
    testlist.SetStringItem(TestItemNo, 1 ,testdb.testname)
    testlist.SetStringItem(TestItemNo, 2 ,' '+str(meaID))
    testlist.SetStringItem(TestItemNo, 3 ,testdb.comments)
    testlist.SetStringItem(TestItemNo, 7 ,testdb.operatorname)
    testlist.SetStringItem(TestItemNo, 8 ,testdb.meatitle)      
    TestItemNo+=1
    if queue_flag_lock:
        testdb.meadb.meaframe.parent._mgr.GetPane(testlist).Caption('Test Queue (Locked)'+' - '+str(TestItemNo)+' untested items')
        testdb.meadb.meaframe.parent._mgr.Update()
    else:
        testdb.meadb.meaframe.parent._mgr.GetPane(testlist).Caption('Test Queue (Unlocked)'+' - '+str(TestItemNo)+' untested items')
        testdb.meadb.meaframe.parent._mgr.Update()


def CheckQueue():
    if TestItemNo>0:    
        testdb=TestQueue[0]
        queue_flag_lock=testdb.meadb.meaframe.parent.queue_flag_lock
        queue_flag_greenOn=testdb.meadb.meaframe.parent.queue_flag_greenOn

    if TestItemNo>0 and not queue_flag_lock and not queue_flag_greenOn:
        code=wx.MessageBox('There are still untested items in the queue.\nContinue to test?\n\nClick Yes to continue.\nClick No to cancel and lock the queue.','Notice',wx.YES_NO)
        if code == wx.YES:
            eval('Test.test'+str(testdb.meadb.meaID)+'.StartTest(testdb.testinstance,testdb)')     
        else:
            testdb.meadb.meaframe.parent.QueueLock()
            
    elif TestItemNo>0 and queue_flag_lock and not queue_flag_greenOn:
        code=wx.MessageBox('The test queue is locked.\nUnlock the queue before testing.','Notice',wx.OK)

    elif TestItemNo>0 and not queue_flag_lock and queue_flag_greenOn:
        eval('Test.test'+str(testdb.meadb.meaID)+'.StartTest(testdb.testinstance,testdb)')
    else:
        pass
#    eval('RawPanel.RawPanel')(parent, name)      

class TestdbGenerator():    
    def __init__(self, testinstance, meadb, equipment, mode = 'new'):
        self.testinstance=testinstance
        self.meadb=meadb
        self.equipment=equipment
        self.testname = ""
        self.operatorname = ""
        self.comments = ""
        self.testinglog = ""
        self.starttime=''
        self.stoptime=''
        self.totaltime=''
        self.meatitle=self.meadb.meaname
        self.filename='' ## This is the raw data file name that we will save to the directory.
        self.test_tagid=-1
        self.treeID=None
        self.rawdata={}
        self.rawpanel_exist = False
        
        if mode == 'new':
            self.testname=self.meadb.meaframe.tcs1.GetValue() #+'('+str(test_tagid+1)+')'+
            self.operatorname=self.meadb.meaframe.tcs5.GetValue()
            self.comments=self.meadb.meaframe.tcs6.GetValue()
            self.testinglog=self.meadb.meaframe.tcs7.GetValue()
