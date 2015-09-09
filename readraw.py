import pickle
import os
print("input the file name:")
filename=raw_input()
tempfile=open(os.path.join(os.getcwd(),'rawdata')+"\\"+filename,'rb')
test=pickle.load(tempfile)
tempfile.close()
