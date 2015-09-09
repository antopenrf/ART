
import pickle

import MeaCase
import MeaDB


def ExportRaw(meaID, export_file, data):
    if meaID in (912, 111):
        data_to_write = zip(data['x'], data['y'])
        export_file.write("MHz" + "\t" + "dB" + "\n")
        for each in data_to_write:
            to_be_written = "{0} \t{1:.6f}\n".format(each[0], each[1]) 
            export_file.write(to_be_written)
        
    export_file.close()

def LoadProject(parent, project):
    saved_list = project.saved_meadbs  ## This is the self.saved_meadb dict under SavedProj class.
    for k, each in enumerate(saved_list.values()):
        saved_meadb = each
        selectedID = saved_meadb.meaID
        selectedType = saved_meadb.meatype
        name = saved_meadb.meaname
        name = name[name.find(".") + 2:]
        eval('MeaCase.CrtMea'+str(selectedID))(parent, selectedType, selectedID, name)
        meaframe = MeaDB.MeaDBList[k].meaframe
        meadb = MeaDB.MeaDBList[k]
        meadb.iPara = saved_meadb.iPara
        meadb.iEqpPara = saved_meadb.iEqpPara
        meadb.iFreq = saved_meadb.iFreq
        telf = meaframe.panelW
        ## Update Measurement Setup and Equipment Setup on PanelW of the MeaPanel object.
        meaframe.Update_MeaSetup(telf, selectedID, saved_meadb.iPara, saved_meadb.iEqpPara)
        meaframe.Update_EqpSetup(telf, selectedID, saved_meadb.iPara, saved_meadb.iEqpPara)
        meaframe.UpdateFreqChkBox()
        ## Update Info page on PanelW.
        meaframe.tcs1.SetValue(saved_meadb.testname)
        meaframe.tcs5.SetValue(saved_meadb.operatorname)
        meaframe.tcs6.SetValue(saved_meadb.comments)
        meaframe.tcs7.SetValue(saved_meadb.testinglog)

        

class SavedDB(object):
    def __init__(self, meadb):
        self.meatype = meadb.meatype
        self.meaID = meadb.meaID
        self.meaname = meadb.meaname
        self.iEqpPara = meadb.iEqpPara
        self.iPara = meadb.iPara
        self.iFreq = meadb.iFreq
        self.testname = meadb.testname
        self.operatorname = meadb.operatorname
        self.comments = meadb.comments
        self.testinglog = meadb.testinglog


class SavedProj(object):
    def __init__(self, meadblist):
        self.saved_meadbs = {}
        k = 1
        for each_db in meadblist:
            self.saved_meadbs[k] = SavedDB(each_db)
            k += 1
