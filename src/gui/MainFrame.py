#coding=utf-8
__author__ = 'ding'
import wx
import os
import sys
import subprocess
import threading
import json
import traceback
import time
from SplitterWindowEx import SplitterWindowEx

class MainFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000,800))
        self.__initGUI__()
        self.Show(True)
        self._proxyStatus = 'stop'
        self._proxyProcess = None
        self.index = 0
        self.data = {}

    def __initGUI__(self):
        self.menu = wx.MenuBar()
        self.fileMenu = wx.Menu()
        menuAbout = self.fileMenu.Append(wx.ID_ANY,'关于')
        menuExit = self.fileMenu.Append(wx.ID_ANY,'离开')
        self.toolsMenu = wx.Menu()
        menuStartProxy = self.toolsMenu.Append(wx.ID_ANY,'开启代理')
        menuStopProxy = self.toolsMenu.Append(wx.ID_ANY,'关闭代理')
        self.menu.Append(self.fileMenu,'文件')
        self.menu.Append(self.toolsMenu,'工具')
        self.SetMenuBar(self.menu)

        self.Bind(wx.EVT_MENU,self.startProxy,menuStartProxy)
        self.Bind(wx.EVT_MENU,self.stopProxy,menuStopProxy)


        self.mainWindow = wx.SplitterWindow(self,wx.ID_ANY,style = wx.SP_LIVE_UPDATE|wx.SP_3D)
        self.upWindow = wx.SplitterWindow(self.mainWindow,wx.ID_ANY,style = wx.SP_LIVE_UPDATE|wx.SP_3D)
        style = wx.LC_REPORT | wx.BORDER_NONE | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING
        self.listCtrlRequests = wx.ListCtrl(self.upWindow,wx.ID_ANY,wx.DefaultPosition,wx.DefaultSize,style)
        self.listCtrlRequests.InsertColumn(0,'No.',width=50)
        self.listCtrlRequests.InsertColumn(1,'Method',width=50)
        self.listCtrlRequests.InsertColumn(2,'Url',width=200)
        self.listCtrlRequests.InsertColumn(3,'Status',width=40)
        self.listCtrlRequests.InsertColumn(4,'Type',width=100)

        requestDetail = wx.Window(self.upWindow,wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.textCtrlRequest = wx.TextCtrl(requestDetail,style=wx.TE_MULTILINE)
        self.textCtrlResponse = wx.TextCtrl(requestDetail,style=wx.TE_MULTILINE)
        sizer.Add(self.textCtrlRequest,1,wx.ALL|wx.EXPAND,border=0)
        sizer.Add(self.textCtrlResponse,1,wx.ALL|wx.EXPAND,border=0)
        requestDetail.SetSizer(sizer)
        self.upWindow.SplitVertically(self.listCtrlRequests,requestDetail,500)

        self.textCtrl = wx.TextCtrl(self.mainWindow, style=wx.TE_MULTILINE|wx.TE_NO_VSCROLL)
        self.mainWindow.SplitHorizontally(self.upWindow,self.textCtrl,-100)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnListSelect,self.listCtrlRequests)
        self.Bind(wx.EVT_CLOSE,self.OnClose)



    def _readProxyErrorProc(self):
        while True:
            if self._proxyProcess == None or self._proxyProcess.poll() != None:
                wx.CallAfter(self.textCtrl.AppendText,'[ERROR] 代理进程不存在，_readProxyErrorProc 线程退出 ')
                break
            data = self._proxyProcess.stderr.readline()
            wx.CallAfter(self.textCtrl.AppendText,data)


    def _readProxyOutputProc(self):
        cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._proxyProcess = subprocess.Popen(sys.executable + ' core/HttpProxy.py',shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE,cwd=cwd)
        wx.CallAfter(self.textCtrl.AppendText,'[INFO] 代理已经启动 Pid: %d\n'%self._proxyProcess.pid)
        threading.Thread(target=self._readProxyErrorProc).start()

        while True:
            if self._proxyProcess.poll() != None:
                wx.CallAfter(self.textCtrl.AppendText,'[ERROR] 代理进程被杀死 Signal: %d\n'%self._proxyProcess.poll())
                self._proxyProcess = None
                break
            data = self._proxyProcess.stdout.readline()
            print 'data',data
            try:
                data  = json.loads(data)
            except:
                sys.stderr.write(traceback.format_exc())
                continue

            request = data['request']
            response = data['response']
            contentType = response['headers'].get('content-type','')
            if contentType.find(';')>-1:contentType = contentType.split(';')[0]
            wx.CallAfter(self.listCtrlRequests.Append,(self.index,request['method'],request['path'],response['code'],contentType))
            self.data[self.index] = data
            self.index += 1





    def startProxy(self,evt):
        if self._proxyProcess != None:
            self.textCtrl.write('[ERROR] 代理已经启动\n')
        self.textCtrl.write('[INFO] 正在启动代理...\n')
        t = threading.Thread(target=self._readProxyOutputProc)
        t.start()
        return t

    def stopProxy(self,evt):
        self.textCtrl.write('[INFO] 正在关闭代理..\n')
        self._proxyProcess.terminate()
        #os.kill(self._proxyProcess.pid,-15)


    def _formatHeaders(self,d):
        ret = ''
        for k in sorted(d.keys()):
            ret += '%s : %s\n'%(k,d[k])
        return ret


    def OnListSelect(self,evt):
        selectIndex = evt.m_itemIndex
        item = self.listCtrlRequests.GetItem(selectIndex)
        index = int(item.GetText())
        data = self.data[index]

        requestInfo = '%s\n%s\n'%(data['request']['path'],data['request']['method'],)
        requestInfo += self._formatHeaders(data['request']['headers'])
        self.textCtrlRequest.SetValue(requestInfo)

        responseInfo = '%s\n'%(data['response']['code'],)
        responseInfo += self._formatHeaders(data['response']['headers'])
        self.textCtrlResponse.SetValue(responseInfo)


    def OnClose(self,evt):
        if self._proxyProcess != None:
            self._proxyProcess.terminate()
        evt.Skip()