__author__ = 'ding'

import wx
from gui.MainFrame import MainFrame


def main():
    app = wx.App(False)
    frame = MainFrame(None, 'PyHttpProxy')
    proxyProcess = frame._proxyProcess
    app.MainLoop()
    if proxyProcess != None: proxyProcess.terminate()




if __name__ == '__main__':
    main()