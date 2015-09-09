import os
import pickle

f = open(os.path.join(os.getcwd(), "rawdata", "temp"), "rb")
p = pickle.load(f)


import vna
v = vna.vna111(17)

