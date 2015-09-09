## positioners.py, starting date: July 24, 2012, written by yulung tang
## This is the module that defines the specific equipment action.
## This module inherits EquipPosi, the positioner equipment-general class.

from controllables import *

class pos311(EquipPosi):
    """equipment-specific class: Positioner: EMCO2090"""
    def startinit(self):
        pass

    def askcurrent(self):
        return self.ask("CP?")

    def asklwrlmt(self):
        return self.ask("LL?")
    
    def askuprlmt(self):
        return self.ask("UL?")

    def wrtseek(self,position):
        self.write("SK %f" % float(position))

    def wrtlwrlmt(self,position):
        self.write("LL %f" % float(position))

    def wrtuprlmt(self,position):
        self.write("UL %f" % float(position))

    def askopc(self):
        return int(self.ask("*OPC?"))

    def wrtskzero(self):
        self.write("SK 0")

    def wrtcpzero(self):
        self.write("CP 0")

    def wrtstop(self):
        self.write("ST")


class pos321(EquipPosi):  #duplicating 2090 driver for Maturo for temp purpose.
    """equipment-specific class: Positioner: EMCO2090"""
    def startinit(self):
        pass

    def askcurrent(self):
        return self.ask("CP?")

    def asklwrlmt(self):
        return self.ask("LL?")
    
    def askuprlmt(self):
        return self.ask("UL?")

    def wrtseek(self,position):
        self.write("SK %f" % float(position))

    def wrtlwrlmt(self,position):
        self.write("LL %f" % float(position))

    def wrtuprlmt(self,position):
        self.write("UL %f" % float(position))

    def askopc(self):
        return int(self.ask("*OPC?"))

    def wrtskzero(self):
        self.write("SK 0")

    def wrtcpzero(self):
        self.write("CP 0")

    def wrtstop(self):
        self.write("ST")
