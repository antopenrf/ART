import sys

class errlog:
    def __init__(self):
        self.logtext=''

    def write(self,errorin):
        self.logtext+=errorin

error=errlog()
save=sys.stdout
sys.stdout=error

import MainGUI


def returnstdout():
    sys.stdout=save
