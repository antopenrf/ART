## controllables.py, starting date: July 24, 2012, written by yulung tang
## This is a module designed to be called by T&M GUI software.
## 'pyvisa' module is imported here and used as the superclass.
## Sep 9, 2015: extending GPIB controml to COM via pyvisa, and LNA via socket.

import visa
from socket import socket, AF_INET, SOCK_STREAM

class EquipCommon():
## class EquipGpib(visa.GpibInstrument): --- pyvisa 1.4 syntax
    """the very top level of GPIB controllables"""
    def __init__(self, address):
        #visa.GpibInstrument.__init__(self,"GPIB::%d" % address)
        self.rm=visa.ResourceManager()
        self.flagOPC=1
        self.connection_type = None
        
        if type(address) == int:
            self.connection_type = 'gpib'
            self.device = self.rm.get_instrument("GPIB::%d" % address)
            
        elif address[:3].lower() == 'com':
            ## Then entered address should be in the format as 'com1', 'com2' ..
            self.connection_type = 'com'
            self.device = self.rm.get_instrument(address)
            
        elif address[:2].lower() == 'ip':
            ## Then entered 'address' should be in the format as "ip xxx.xxx.xxx.xxx port".
            self.connection_type = 'ip'
            ip_address = address.split(" ")
            ip = ip_address [1]
            port = int(ip_address[2])
            self.device = socket(AF_INET, SOCK_STREAM)
            self.device.connect((ip, port))
            

    def write(self, to_be_written):
        if self.connection_type in ['gpib', 'com']:
            return self.device.write(to_be_written)
        else: ## ip connection
            return self.device.send(to_be_written + '\n')
        
    def ask(self, to_be_asked):
        if self.connection_type in ['gpib', 'com']:
            return self.device.ask(to_be_asked)
        else: ## ip connection
            self.device.send(to_be_asked + '\n')
            return self.device.recv(4096)
        
    def read(self):
        if self.connection_type in ['gpib', 'com']:
            return self.device.read()
        else: ## ip connection
            return self.device.recv(4096)
        
    def close(self):
        return self.device.close()
    
    def ifopc(self):
        return self.askopc()
    
    def setname(self,name):
        self.name=str(name)

    def wait_opc(self):
        while not self.ifopc():
            pass

    
# important concept:  The technique of extension is used here to
# seperate the common equipment functionality from specifics of equipment commands.
# Class names starting with 'Equip' provider generic functions seen by 
# GUI, while class names ending with specific equipment models   
# are different drivers not directly seen by GUI.
# Equipment objects will be generated from equipment-specific classes.
# But we use the functions under equipment-general classes to interact with TUI.

# All the equipment-specific classes are stored in sperate files.
# Current avaialble equipment specific classes:
# positioners.py
# vnas.py

        
class EquipPosi(EquipCommon):
    
    """equipment-general class: Positioner """
    def initialization(self):
        self.startinit()
    
    def current(self):
        return self.askcurrent()

    def lwrlmt(self):
        return self.asklwrlmt()
    
    def uprlmt(self):
        return self.askuprlmt()
    
    def mvto(self,position):
        self.wrtseek(position)

    def setlwrlmt(self,position):
        self.wrtlwrlmt(position)

    def setuprlmt(self,position):
        self.wrtuprlmt(position)

    def mvtozero(self):
        self.wrtskzero()

    def crtozero(self):
        self.wrtcpzero()

    def stop(self):
        self.wrtstop()

class EquipVna(EquipCommon):
    
    """equipment-general class: Positioner """
    def initialization(self):
        self.startinit()

    def set_sij(self, sij):
        self.wrt_sij(sij)

    def set_pwr(self, pwr):
        self.wrt_pwr(pwr)

    def set_ifb(self, ifb):
        self.wrt_ifb(ifb)

    def set_pnt(self, pnt):
        self.wrt_pnt(pnt)
        
    def set_single_freq(self, freq):
        self.wrt_single_freq(freq)

    def get_spot_data(self):
        return self.ask_spot_data()

    
