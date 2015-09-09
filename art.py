#!/usr/bin/python
import wx
from MainGUI import *
import thread


app = wx.App()

info()
frame = MainFrame(None)
frame.GPIB_token=thread.allocate_lock()
frame.Show()
    
app.MainLoop()
