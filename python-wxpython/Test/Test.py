# -*- coding: utf-8 -*-

import wx
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class App(wx.App):
    def OnInit(self):
        frame = Frame('2048')
        frame.Center()
        frame.Show()
        return True


class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        self.SetSize(510, 750)
        self.window = Window(self)


class Window(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        w, h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w, h)
        self.bgFont = wx.Font(50, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.scFont = wx.Font(36, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.smFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.Bind(wx.EVT_SIZE, self.on_size)  # use wx.BufferedPaintDC

    def init_buffer(self):
        w, h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w, h)

    def on_size(self, event):
        self.init_buffer()
        self.draw_all()

    def draw_all(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.draw_bg(dc)
        # self.draw_logo(dc)
        # self.draw_label(dc)
        # self.drawScore(dc)
        self.draw_tiles(dc)

    @staticmethod
    def draw_bg(dc):
        dc.SetBackground(wx.Brush((250, 248, 239)))
        dc.Clear()
        dc.SetBrush(wx.Brush((187, 173, 160)))
        dc.SetPen(wx.Pen((187, 173, 160)))
        dc.DrawRoundedRectangle(15, 150, 475, 475, 5)

    def draw_logo(self, dc):
        dc.SetFont(self.bgFont)
        dc.SetTextForeground((119, 110, 101))
        dc.DrawText(u"2048", 15, 26)

    def draw_label(self, dc):
        dc.SetFont(self.smFont)
        dc.SetTextForeground((119, 110, 101))
        dc.DrawText(u"Join the numbers and get to the 2048 tile!", 15, 114)
        dc.DrawText(u"HOW TO PLAY: Use your arrow keys to move the tiles. "
                    u"\nWhen two tiles with the same number touch,\nthey merge into one!", 15, 639)

    def draw_tiles(self, dc):
        dc.SetFont(self.scFont)
        for row in range(4):
            for col in range(4):
                dc.SetTextForeground((119, 110, 101))
                dc.SetBrush(wx.Brush((238, 228, 218)))
                dc.SetPen(wx.Pen((237, 207, 114)))
                dc.DrawRoundedRectangle(35 + col * 115, 165 + row * 115, 90, 90, 50)
                dc.DrawText(str(row + col), 30+col*115 + 38, 165+row*115 + 22)
                # size = dc.GetTextExtent(str(value))

if __name__ == "__main__":
    app = App()
    app.MainLoop()
    # randint = random.randint(0, 1)
    # if randint:
    #     print randint, True
    # else:
    #     print randint, False
