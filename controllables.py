## controllables.py, starting date: July 24, 2012, written by yulung tang
## This is a module designed to be called by T&M GUI software.
## 'pyvisa' module is imported here and used as the superclass.

import visa

class EquipGpib():
#class EquipGpib(visa.GpibInstrument):
    """the very top level of GPIB controllables"""
    def __init__(self,address):
        #visa.GpibInstrument.__init__(self,"GPIB::%d" % address)
        self.rm=visa.ResourceManager()
        self.flagOPC=1
        self.device = self.rm.get_instrument("GPIB::%d" % address)

    def write(self, to_be_written):
        return self.device.write(to_be_written)

    def ask(self, to_be_asked):
        return self.device.ask(to_be_asked)

    def read(self):
        return self.device.read()
    
    def close(self):
        return self.device.close()
    
    def ifopc(self):
        return self.askopc()
    
    def setname(self,name):
        self.name=str(name)
                  
    
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

        
class EquipPosi(EquipGpib):
    
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

class EquipVna(EquipGpib):
    
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

    
