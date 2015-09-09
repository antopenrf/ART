from matplotlib import __version__ as matplotlib_version
from sys import version as python_version
from visa import __version__ as visa_version
from wx import __version__ as wx_version

module_version = {'python': python_version, 'mat': matplotlib_version, 'visa': visa_version, 'wx': wx_version}
software_version = '1.0.0'
rawdata_version = '1.0.0'
