#coding=utf-8
__author__ = 'ding'
import wx


class SplitterWindowEx(wx.SplitterWindow):
    def __init__(self,parent,ID,style = wx.SP_LIVE_UPDATE,keepRate = False):
        wx.SplitterWindow.__init__(self,parent,wx.ID_ANY,style=style,size=parent.Size)
        self.Bind(wx.EVT_SIZE,self.OnSize)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged)

        self.SetMinimumPaneSize(0)
        self.KeepRate = keepRate


    def Init(self,len1,len2,isVertical):
        self.len1 = len1
        self.len2 = len2
        self.isVertical = isVertical

        if isVertical:
            width1 = 1.0*len1/(len1+len2)* self.Parent.Size.width
            width2 = self.Parent.Size.width - width1
            self.w1 = wx.Window(self,size = (width1, self.Parent.Size.height), pos = (0,0))
            self.w2 = wx.Window(self,size = (width2, self.Parent.Size.height), pos = (width1+1,0))
            self.SplitVertically(self.w1, self.w2, 100)
        else:
            height1 = 1.0*len1/(len1+len2)*self.Parent.Size.height
            height2 = self.Parent.Size.height - height1
            self.w1 = wx.Window(self,size = (self.Parent.Size.width,height1), pos = (0,0))
            self.w2 = wx.Window(self,size = (self.Parent.Size.width,height2), pos = (0,height1+1))
            self.SplitHorizontally(self.w1, self.w2, 100)

        print self.w1.Position,self.w1.Size
        print self.w2.Position,self.w2.Size


    def OnSize(self,event):
        #保持窗口划分比例
        if self.KeepRate:

            if self.SplitMode == 2:
                #水平切分
                width1 = 1.0*self.len1/(self.len1+self.len2)* event.Size.width
                self.SetSashPosition(width1)
            elif self.SplitMode == 1:
                #垂直切分
                height1 = 1.0*self.len1/(self.len1+self.len2)* event.Size.height
                self.SetSashPosition(height1)
                #print 'sash:',height1,self.SashPosition

            print 'size change',event.Size,'sash',self.GetSashPosition(),'len1,len2',self.len1,self.len2
            print 'w1',self.w1.Position,self.w1.Size
            print 'w2',self.w2.Position,self.w2.Size

    def OnSashChanged(self,event):
        #记录比例
        self.len1 = event.GetSashPosition()

        if self.isVertical:
            self.len2 = self.Size.width - self.len1
        else:
            self.len2 = self.Size.height - self.len1

        print 'sash changed:',self.len1,self.len2

if __name__ == '__main__':
    app = wx.App(False)
    window = wx.Frame(None,-1,'test')
    sw = SplitterWindowEx(window,-1,keepRate=False)
    sw.Init(10,20,True)
    sw.w1.SetBackgroundColour('pink')
    sw.w2.SetBackgroundColour('black')
    window.Show()
    app.MainLoop()