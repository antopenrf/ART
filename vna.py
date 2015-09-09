### This is the module to directly access the control of VNA equipment.
###
### For example:  To access ENA5071C at GPIB address = 17, instantiate as
###               ena = vna111(17)
###
### Either control directly:
###
###               ena.ask("*IDN?")
###               ena.write("SYST:RPES")
###               
### or use defined function:
###
###               ena.startinit()

### To add drivers, both of this vna.py and controllables.py need to be edited.

from controllables import *

class vna121(EquipVna):
    """equipment-specific class: VNA: R&S ZVL"""
    def startinit(self):
        pass


class vna111(EquipVna):
    """equipment-specific class: VNA: ENA 5071C"""
    def startinit(self):
        self.write("SYST:PRES")

    def askopc(self):
        return int(self.ask("*OPC?"))

    def wrt_sij(self, sij):
        self.write(":CALC1:PAR1:DEF {s}".format(s = sij))

    def wrt_pwr(self, pwr):
        self.write(":SOUR1:POW {p}".format(p = pwr))

    def wrt_ifb(self, ifb):
        self.write(":SENS1:BAND {f}".format(f = ifb))

    def wrt_pnt(self, pnt):
        self.write(":SENS1:SWE:POIN {p}".format(p = pnt))
        
    def wrt_single_freq(self, freq):
        self.write(":SENS1:FREQ:STAR {f}".format(f = freq))
        self.write(":SENS1:FREQ:STOP {f}".format(f = freq))

    def ask_spot_data(self):
        self.write(":DISP:WIND1:TRAC1:Y:AUTO")
        self.write(":FORM:DATA ASC")
        self.write(":TRIG:SOUR BUS")
        self.write(":TRIG:SING")
        while not self.ask("*OPC?"):
            pass
        return float(str(self.ask("CALC1:DATA:FDAT?")).split(",")[0])
