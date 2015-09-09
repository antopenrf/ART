import version

class DatadbGenerator():
    def __init__(self,testdb):
            self.filename=testdb.filename
            self.data=testdb.rawdata
            self.testname=testdb.testname
            self.test_tagid=testdb.test_tagid
            self.equipment=testdb.equipment
            self.starttime=testdb.starttime
            self.stoptime=testdb.stoptime
            self.totaltime=testdb.totaltime
            self.operatorname=testdb.operatorname
            self.comments=testdb.comments
            self.testinglog=testdb.testinglog
            self.meatitle=testdb.meatitle
            self.meatype=testdb.meadb.meatype
            self.meaID=testdb.meadb.meaID
            self.meacount=testdb.meadb.count
            self.iEqpPara=testdb.meadb.iEqpPara
            self.iPara=testdb.meadb.iPara
            self.iFreq=testdb.meadb.iFreq    

            
            self.versions = {}
            self.versions['modules'] = version.module_version
            self.versions['software'] = version.software_version
            self.versions['rawdata'] = version.rawdata_version
