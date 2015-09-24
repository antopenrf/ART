# -*- coding: cp950 -*- (obselete)
#---------------------------------abstract
# This module is designed to run all the tests taken from the measurement panle.
# Each specific test case is given a 3 digit number, for example: 212.
# The 1st digit is give per the measurement category.
# The 2nd digit is given per the measurement group.
# The 3rd digit is given per the test case.
# The class heirarchy is test(top) <-- test2 (level.1) <-- test21 (level.2) <-- test212(level.3).
# test.__init__ starts all basic checks, such as equipment assignments (overriden by test2), GPIB addressing (overriden by test2), instrument identity, parameter completeness  (overriden by test212).
# All possible instrumentation control commands are coded under level.1; the final testing loop is coded under level.3.


#---------------------------------importing
import visa
import thread
from instruments import *
from CrtWidget import *
import Queue
queuelist=Queue.Queue
import time
import TestCore
core111 = TestCore.core111
import TestDB 
from math import pi
from math import sin
from socket import error as socket_error
#---------------------------------coding
        
rm_in_Test = visa.ResourceManager()


class test(object):
    run_in_spawn = False
    number_of_spawn = 0
    AutoApply = True
    def __init__(self,meadb):
        self.meadb=meadb
        self.meaframe=meadb.meaframe
        self.meaid=meadb.meaID
        self.eqplist=self.meadb.iEqpPara ## important: refering to EqpConfig stored in the eqpsetup.ini.
        self.freq=self.meadb.iFreq       ## important: test frequencies
        self.para=meadb.iPara[str(self.meaid)]  ## important: measuremnet parameters
        self.gpiblist=[]
        self.equipment={} #This is the dictionary stores the equipment name (such as pos1, pos2) in keys, with the eval commands in values (such as pos311(gpib no)). 
        self.queue_lock=self.meaframe.parent.queue_flag_lock #the flag to indicate the queue is locked (1) or not (0)
        #define four checkup flags
        self.flag_Assignment=1
        self.flag_GPIB=0
        self.flag_Instrument=0
        self.flag_Parameter=1
        #define all green lights flag when four checkups are done        
        self.flag_AllGreenLights=0
  
        #### Starting the routine of four (4) main Checkups ####
        #The method within test class level 1.  Check if all the equipments are assigned and GPIB address are given.  Equipments identity (*IDN?) not checked here.
        self.Dialog=CheckingDialog(self.meaframe.parent)
        self.CheckAssignment()   #--> CheckGPIB --> CheckInstrument --> CheckParameter
        
        ## Codes to run without equipments in presence
        #self.flag_AllGreenLights=0
        #self.OnSetAfterFourChecks()

                    
    def OnSetAfterFourChecks(self):      
        def QueueUp():
            self.flag_AllGreenLights=1

            if test.run_in_spawn:
                comments = self.meadb.meaframe.tcs6
                for each in range(1, test.number_of_spawn+1):
                    comments.AppendText("--- Spawn no. " + str(each))
                    testdb = TestDB.TestdbGenerator(self, self.meadb, self.equipment)
                    testdb.comments = comments.GetValue()
                    comments.Remove(comments.GetLastPosition()-len(str(each))-14, comments.GetLastPosition())
                    TestDB.TestDBadd(testdb)
                test.run_in_spawn = False
                test.number_of_spawn = 0
                    
            ###---generate the test data base to be added to the queue later---###
            elif TestDB.TestItemNo==0 and not self.queue_lock:
                code=wx.MessageBox('Click OK to start the test.','Notice',wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
                if code == wx.OK:
                    testdb=TestDB.TestdbGenerator(self,self.meadb,self.equipment)
                    TestDB.TestDBadd(testdb)                    
                    self.StartTest(testdb)
                else:
                    pass
 
            elif TestDB.TestItemNo==0 and self.queue_lock:
                code=wx.MessageBox('Test queue is locked.\nAdd the test item to the queue?','Notice',wx.YES_NO)
                if code == wx.YES:
                    testdb=TestDB.TestdbGenerator(self,self.meadb,self.equipment)
                    TestDB.TestDBadd(testdb)
                else:
                    pass                

                    
            elif TestDB.TestItemNo>0:
                code=wx.MessageBox('There are untested items in the test queue.\nAdd the test item to the queue?','Notice',wx.YES_NO)
                if code == wx.YES:
                    if TestDB.TestItemNo==0 and not self.queue_lock:
                        testdb=TestDB.TestdbGenerator(self,self.meadb,self.equipment)
                        TestDB.TestDBadd(testdb)
                        TestDB.CheckQueue()
                    else:
                        testdb=TestDB.TestdbGenerator(self,self.meadb,self.equipment)
                        TestDB.TestDBadd(testdb)
                else:
                    pass
                
        self.Dialog.Completed('Verfication is all done and completed.\nClick Ok to continue, or Cancel to leave.', QueueUp)     
        

    def CheckAssignment(self):####Check 1, overriden in level1.
        self.Dialog.Updating('Starting to verify equipment assignment...')    
        time.sleep(1)


    def CheckGPIB(self,token):####Check 2, coded herein in top level.
        self.Dialog.Updating('Equipment assignment is validated.\nStarting to verify GPIB address assignment...')
        time.sleep(1)       
        def extract(item):
            if type(item)!=list:
                if item != None:
                    self.gpiblist.append(item)#####????? here excepts !
            else:
                for x in item:
                    extract(x)
                    
        #Get currently assigned GPIB address from self.eqplist.
        templist = []
        for each1 in self.para['eqp']:
            the_eqp = self.eqplist[each1]
            if the_eqp['_CTRL1'] == 'GPIB':
                templist=the_eqp['_GPIB']
                extract(templist)
                
        if templist == []:
            self.flag_GPIB=1
            thread.start_new_thread(self.CheckInstrument,(self.meaframe.GPIB_token,))

        else:
            ## Get the currently connected instruments from pyvisa.
            connected=[]
            token.acquire()#Token ------- Acquire the lock token to encapsulate the routine that invloves accessing with GPIB interface.
            visaconnected = rm_in_Test.list_resources()  ### previously: visa.get_instruments_list()
            visaconnected = [ str(each) for each in visaconnected ]  ## Convert from unicode to string for Python2.x
            token.release()#Token ------- Release the lock token to encapsulate the routine that invloves accessing with GPIB interface.
            for each in visaconnected:
                if each[:4]=='GPIB':
                    connected.append(int(each[7:-7]))
                    ## Check if the assigned GPIB addresses are all in the currently-connected list.
            nonconnected=[]
            nonconnectedstring=''
            for each1 in self.gpiblist:
                flag=0
                for each2 in connected:
                    if each1==each2:
                        flag=1
                if not flag:
                    nonconnected.append(each1)
                    nonconnectedstring+=('('+str(each1)+') ')
            if nonconnected == []:
                self.flag_GPIB=1
            else:
                self.flag_GPIB=0

            #Check if there is duplicated GPIB address.
            if duplicateditem(self.gpiblist) != []:
                self.Dialog.Uncompleted("There are duplicated GPIB address assignments.\nPlease check the configuration again.")
            else:
                if not self.flag_GPIB:
                    self.Dialog.Uncompleted("GPIB address of " + nonconnectedstring + "are not found activated.\nPlease check  configuration or GPIB cable connection.")

            if self.flag_GPIB:
                #The method within test class level top.  Start generationg the equipment list that stores all the equipment pieces which will be used during the testing.  Equipments identity (*IDN?) will be checked here.
                thread.start_new_thread(self.CheckInstrument,(self.meaframe.GPIB_token,))        

    def CheckInstrument(self,token):####Check 3, coded herein in top level.
        self.Dialog.Updating('Communication address assignment is validated.\nStarting to verify equipment identification...')
        time.sleep(1)

        if self.flag_GPIB and self.flag_Assignment:          
            self.flag_Instrument=1

            ## There are two loops: 1st is for different equipment types, such as vna, pos.
            ## The 2nd loop is for the number of the same device. Looping through nod.
            for each_eqp in self.para['eqp']:    ### loop 1
                ##### --- Prepare equipment comm address list. --- #####
                the_eqp = self.eqplist[each_eqp]  ## eqplist is meadb.iEqpPara.
                nod = the_eqp['nod']
                gpib_list = self.eqplist[each_eqp]['_GPIB']
                if type(gpib_list) != list:
                    gpib_list = [gpib_list, ]
                com_list = self.eqplist[each_eqp]['_COM']
                if type(com_list) != list:
                    com_list = [com_list, ]
                ip_list = self.eqplist[each_eqp]['_IP']
                if type(ip_list) != list:
                    ip_list = [ip_list, ]
                comm_list = []
                if nod == None:
                    nod = 1
                for each in range(nod):
                    ctrl = '_CTRL' + str(each + 1)
                    if the_eqp[ctrl] == 'GPIB':
                        comm_list.append(str(gpib_list[each]))
                    elif the_eqp[ctrl] == 'COM':
                        comm_list.append('com'+str(com_list[each]))
                    else:
                        comm_list.append("\"ip " + str(ip_list[each]) + "\"")
                if nod == 1:
                    comm_list = comm_list[0]
                            
                for n, each_comm in enumerate(makelist(comm_list)):          ### loop 2
                    ## The number of available '_GPIB' address determined the number of this for-loop
                    n = n + 1
                    if each_comm != None:
                        ### Token ------- Acquire the lock token to encapsulate the routine that invloves accessing with GPIB interface.
                        token.acquire()
                        
                        #*** -- This is where we initiate instrument from EquipCommon.
                        evalstring = each_eqp + str(self.eqplist[each_eqp]['eqpno'])+'(' + each_comm + ')'
                        if evalstring.find('ip'):
                            try:
                                temp = eval(evalstring)
                            except socket_error:
                                self.Dialog.Uncompleted("Equipment [%s] addressed at [%s] \nis not communicating.\nPlease check equipment configuration." %(self.eqplist[each_eqp]['eqpname'], each_comm[3:]))
                                self.flag_Instrument = 0
                                token.release()
                        else:
                            temp=eval(evalstring)
                        #*** ---------------------------------------------------------

                        if self.flag_Instrument:
                            tempIDN = temp.ask("*IDN?").find(EqpIDN[self.eqplist[each_eqp]['eqpno']])
                            temp.close()
                            token.release()
                        ### Token ------- Release the lock token to encapsulate the routine that invloves accessing with GPIB interface.
                            if tempIDN==-1:
                                self.Dialog.Uncompleted("Equipment [%s] addressed at [%s] is not identified.\nPlease check equipment configuration." %(self.eqplist[each_eqp]['eqpname'],each_comm))
                                self.flag_Instrument=0
                            else:
                                self.equipment[each_eqp+str(n)]=evalstring
                            ##This is the evaluation string we use to generate the pyvisa instance for GPIB interface.

        ##The following method is under test class level 3.  Check if all necessary parameters are given.
        if self.flag_Instrument:
            self.CheckParameter()
        
    def CheckParameter(self):####Check 4, overriden in level 3.
        self.Dialog.Updating('Equipment identification is validated.\nStarting to verify testing parameters...')
        time.sleep(1)         
    
    def _OnIdle(self,event):
        wx.WakeUpIdle()
        if not self.updating_queue.empty():
            dataitem=self.updating_queue.get()
            self.meaframe.tcs7.AppendText(dataitem)
        else:
            pass
        
    def StartTest(self):
        pass                    

    def TestLoop_Start(self,testdb):
        temptime=time.localtime()
        testdb.starttime=time.strftime("%H:%M:%S   %m/%d/%Y",temptime)
        testdb.totaltime=time.time()
        self.meaframe.parent.testlist.SetStringItem(0,4,testdb.starttime)     

    def TestLoop_Stop(self,testdb):
        temptime=time.localtime()
        if testdb.testname == '':
            underscore = ''
        else:
            underscore = '_'
        testdb.filename=time.strftime("%Y.%m.%d_%Hh_%Mm%S",temptime) + underscore + testdb.testname
        testdb.stoptime=time.strftime("%H:%M:%S   %m/%d/%Y",temptime)
        testdb.totaltime=time.time()-testdb.totaltime
        ttl = testdb.totaltime
        days = int(ttl.__int__()/86400)
        hours = int((ttl.__int__() - 86400*days)/3600)
        minutes = int((ttl.__int__() - 86400*days - 3600*hours)/60)
        seconds = int((ttl.__int__() - 86400*days - 3600*hours - 60*minutes))
        totaltimestring=str(days) + 'd '+str(hours) +'h '+ str(minutes) +'m '+ str(seconds)+'s'
        self.meaframe.parent.testlist.SetStringItem(0,5,testdb.stoptime)
        self.meaframe.parent.testlist.SetStringItem(0,6,totaltimestring)       
        if not self.meaframe.parent.queue_flag_greenOn:
            OkBox('Test ' + str(testdb.meadb.meaID) + 'completed!')
        else:
            pass        
        TestDB.TestDBremove()
        TestDB.CheckQueue()
        self.meadb.meaframe.panelW.Enable()

    def Apply_Correction(self, meadb, xdata, ydata):
        loaded_path = meadb.iPara[str(meadb.meaID)]["_Correction"]
        if loaded_path == "":
            pass
        else:
            if not test.AutoApply:
                code=wx.MessageBox('Correction file exists.  Apply correction?','Notice',wx.YES_NO)
                if code == wx.YES:
                    loaded_file = file(loaded_path, "rb")
                    correction = pickle.load(loaded_file).data
                    c_xdata = correction['x']
                    c_ydata = correction['y']
                    if c_xdata != xdata:
                        wx.MessageBox('Frequencies not matched!  No correction applied!','Notice',wx.CANCEL)
                    else:
                        for k, each in enumerate(ydata):
                            ydata[k] = ydata[k] - c_ydata[k]
            else:
                loaded_file = file(loaded_path, "rb")
                correction = pickle.load(loaded_file).data
                c_xdata = correction['x']
                c_ydata = correction['y']
                if c_xdata != xdata:
                    wx.MessageBox('Frequencies not matched!  No correction applied!','Notice',wx.CANCEL)
                else:
                    for k, each in enumerate(ydata):
                        ydata[k] = ydata[k] - c_ydata[k]
            meadb.meaframe.plotter.drawgraph( xdata, ydata)
            

            
##### --- Test Category 2 --- #####
class test2(test):
    def __init__(self,meadb):
        test.__init__(self,meadb) 


    def CheckAssignment(self):
        test.CheckAssignment(self)
        if self.eqplist['vna']['eqpno']==None:
            self.Dialog.Uncompleted("No VNA is assigned.")
            self.flag_Assignment=0
        if self.eqplist['pos']['eqpno']==None:
            self.Dialog.Uncompleted("No Positioner is assigned.")
            self.flag_Assignment=0
        if self.eqplist['vna']['_GPIB']==None and self.eqplist['vna']['_COM']==None and self.eqplist['vna']['_IP']==None:
            self.Dialog.Uncompleted("No address is assigned to VNA.\nPlease check the parameters.")
            self.flag_Assignment=0
        if self.eqplist['pos']['_GPIB'][0]==None and self.eqplist['pos']['_COM'][0]==None and self.eqplist['pos']['_IP'][0]==None:
            self.Dialog.Uncompleted("No address is assigned to the primary positioner.\nPlease check the parameters.")
            self.flag_Assignment=0
#        if self.para['value'][1]=='Yes':
#            if self.eqplist['pos']['_GPIB'][1]==None:
#                self.Dialog.Uncompleted("No positioner GPIB address is assigned to the secondary positioner..\nPlease check the parameters.")
#                self.flag_Assignment=0
        if self.flag_Assignment:
            ## The method within test class level 1.  Check if the assigned GPIB address are communicating.  
            thread.start_new_thread(self.CheckGPIB,(self.meaframe.GPIB_token,))

        
    def Cmd_Sk_Pos(self,device,position):
        device.wrtseek(position)
        self.flag_pos_OPC=0 
        while not device.ifopc():
            text='Rotating ...\n' + 'Theta position: ' + str(float(device.current())) +'\n'
            self.updating_queue.put(text)
            self.updating_list.append(text)
        self.flag_pos_OPC=1


    def Cmd_Sk_DualPos(self,device1,device2,position):
        self.flag_dualpos_OPC=0
        self.meaframe.GPIB_token.acquire()
        device1.wrtseek(position[0])
        device2.wrtseek(position[1])
        while not device1.ifopc() or not device2.ifopc():
            text='Rotating ...\n' + 'Theta position: ' + str(float(device1.current())) +'\n' + 'Phi position: ' + str(float(device2.current())) + '\n\n'
            self.updating_queue.put(text)
            self.updating_list.append(text)
            time.sleep(0.1)
        self.meaframe.GPIB_token.release()
        self.flag_dualpos_OPC=1 


class test21(test2):
    def __init__(self,meadb):
        test2.__init__(self,meadb)


class test212(test21):
    def __init__(self,meadb):
        test21.__init__(self,meadb)
            
    def CheckParameter(self):
        test.CheckParameter(self)

        if self.freq==[]:
            self.Dialog.Uncompleted("Frequency list is empty.\nPlease check the parameters.")
            self.flag_Parameter=0
        if self.para['_PrimaryStep']==0:
            self.Dialog.Uncompleted("Rotation step can not be zero.\nPlease check the parameters.")
            self.flag_Parameter=0
        if self.flag_Parameter:
            self.OnSetAfterFourChecks()

    def TestLoop(self,pos1,pos2,testdb):
        ### Begining of the test loop.
        self.TestLoop_Start(testdb)

        self.meadb.meaframe.panelW.Disable()
        ### Testing-specific loop
        pos1step=self.para['_PrimaryStep']
        pos2fixed=self.para['_SecondaryFixed']
        self.Cmd_Sk_DualPos(pos1,pos2,(0,pos2fixed))

        for n in range(x):
            self.Cmd_Sk_DualPos(pos1, pos2, (0,360/x*n))
            
            ## - TestCore.core111 test routine - ###
            testdb.rawdata['x'], testdb.rawdata['y'] = core111(self.vna, self.freq, mode = 'plotter', plotter = self.meaframe.plotter)

        
        self.meadb.flag_in_Testing=0
        self.vna.close()
        self.pos1.close()
        self.pos2.close()

        ### End of the test loop.        
        self.TestLoop_Stop(testdb)

        
    def StartTest(self,testdb):
        self.updating_queue=queuelist()
        self.updating_list=[]
        self.meaframe.Bind(wx.EVT_IDLE,self._OnIdle)
        ## Bind each specific measurement frame with the idle event
        ## in order to automatically update the testing updates.
    ####----Initialization of equipments are put under the initial onset of the TestLoop of level.3 class.
    ####----For test212, the equipments are given as pos1, pos2, vna.    
        if self.para['value'][1]=='Yes':
            self.flag_2ndpos=True
        else:
            self.flag_2ndpos=False

        self.vna=eval(self.equipment['vna1'])
        self.pos1=eval(testdb.equipment['pos1'])
        self.pos1.setname=self.para['value'][0]
        if self.flag_2ndpos:
            self.pos2=eval(testdb.equipment['pos2'])
            self.pos2.setname=self.para['value'][2]
    #end----Initialization of equipments



    ####----Starting the test loop.
        if self.flag_AllGreenLights:   
            
            self.meadb.flag_in_Testing=1
            thread.start_new_thread(self.TestLoop, (self.pos1, self.pos2, testdb))




            
##### --- Test Category 1 --- #####
class test1(test):
    def __init__(self,meadb):
        test.__init__(self,meadb) 

    def CheckAssignment(self):
        test.CheckAssignment(self)
        the_eqp = self.eqplist['vna']
        if the_eqp['eqpno']==None:
            self.Dialog.Uncompleted("No VNA is assigned.")
            self.flag_Assignment=0

        if the_eqp['_GPIB']==None and the_eqp['_COM']==None and the_eqp['_IP']==None:
            self.Dialog.Uncompleted("No communication address is assigned to VNA.\nPlease check the parameters.")
            self.flag_Assignment=0

        if self.flag_Assignment:
            #The method within test class level 1.  Check if the assigned GPIB address are communicating.  
            thread.start_new_thread(self.CheckGPIB,(self.meaframe.GPIB_token,))

            
class test11(test1):
    def __init__(self,meadb):
        pass
        ##        test2.__init__(self,meadb)


        
class test111(test11):

    def __init__(self, meadb):
        test1.__init__(self, meadb)
            
    def CheckParameter(self):
        test.CheckParameter(self)

        if self.freq==[]:
            self.Dialog.Uncompleted("Frequency list is empty.\nPlease check the parameters.")
            self.flag_Parameter=0

        if self.flag_Parameter:
            self.OnSetAfterFourChecks()

    def TestLoop(self, testdb):
        ### --- Begining of the test loop.
        self.TestLoop_Start(testdb)
        
        ### -- Testing-specific settings -- ###
        sij = self.para['value'][0].split()
        pin = self.eqplist['vna']['_PWR'][0]
        ifb = self.eqplist['vna']['_IFB']
        
        self.vna.initialization()
        self.vna.wait_opc()

        self.vna.set_pnt(1)
        self.vna.set_sij(sij)
        self.vna.set_pwr(pin)
        self.vna.set_ifb(ifb)

        self.meadb.meaframe.panelW.Disable()
        ## - TestCore.core111 test routine - ###
        testdb.rawdata['x'], testdb.rawdata['y'] = core111(self.vna, self.freq, mode = 'plotter', plotter = self.meaframe.plotter)


        self.Apply_Correction(self.meadb, testdb.rawdata['x'], testdb.rawdata['y'])
        
        self.meadb.flag_in_Testing=0
        self.vna.close()

        ### --- End of the test loop.
        
        self.TestLoop_Stop(testdb)


    def StartTest(self,testdb):
        self.updating_queue=queuelist()
        self.updating_list=[]
        self.meaframe.Bind(wx.EVT_IDLE,self._OnIdle)  #to bind each specific measurement frame with the idle event to automatically update the testing updates
    ####----Initialization of equipments are put under the initial onset of the TestLoop of level.3 class.
    ####----For test111, the equipments are given as only vna.    

        self.vna=eval(testdb.equipment['vna1'])

    #end----Initialization of equipments
        sij = self.para['value'][0]


    ####----Starting the test loop.
        if self.flag_AllGreenLights:   
            
            self.meadb.flag_in_Testing=1
            thread.start_new_thread(self.TestLoop,(testdb, ))


    
            
##### --- Test Category 9: demo only --- #####
class test9(test):
    def __init__(self,meadb):
        self.meadb=meadb
        self.meaframe=meadb.meaframe
        self.meaid=meadb.meaID
        self.eqplist=self.meadb.iEqpPara ## important: refering to EqpConfig stored in the eqpsetup.ini.
        self.freq=self.meadb.iFreq       ## important: test frequencies
        self.para=meadb.iPara[str(self.meaid)]  ## important: measuremnet parameters
        self.gpiblist=[]
        self.equipment={} #This is the dictionary stores the equipment name (such as pos1, pos2) in keys, with the eval commands in values (such as pos311(gpib no)). 
        self.queue_lock=self.meaframe.parent.queue_flag_lock #the flag to indicate the queue is locked (1) or not (0)

        #define all green lights flag when four checkups are done        
        self.flag_AllGreenLights=0
        self.Dialog=CheckingDialog(self.meaframe.parent)


        ##self.OnSetAfterFourChecks() ## OnSet after Check_Parameter is done.
        

class test912(test9, test111):

    def __init__(self, meadb):
        test9.__init__(self, meadb)
        self.flag_Parameter = 1
        self.CheckParameter()
        self.meadb = meadb

    def TestLoop(self, testdb):
        ### Begining of the test loop.
        self.TestLoop_Start(testdb)
        
        ### Testing-specific loop
        k = len(self.freq)
        
        for n in range(k):
            anglelist = [ 2*pi/k*each for each in range(n+1)]
            ydata = map(lambda y:sin(y)**2, anglelist)
            xdata = self.freq[:(n+1)]
            time.sleep(0.01)
            self.meaframe.plotter.drawgraph( xdata, ydata) 

        self.Apply_Correction(self.meadb, xdata, ydata)
        
        testdb.rawdata['x'] = xdata
        testdb.rawdata['y'] = ydata
        
        self.meadb.flag_in_Testing=0
        ### End of the test loop.        
        self.TestLoop_Stop(testdb)
        
    def StartTest(self,testdb):
        self.updating_queue=queuelist()
        self.updating_list=[]
        self.meaframe.Bind(wx.EVT_IDLE,self._OnIdle)

    ####----Initialization of equipments are put under the initial onset of the TestLoop of level.3 class.
    ####----For test912, the equipments are given none
    #end----Initialization of equipments


    ####----Starting the test loop.
        if self.flag_AllGreenLights:   
            
            self.meadb.flag_in_Testing=1
            thread.start_new_thread(self.TestLoop, (testdb, ))

