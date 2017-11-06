# -*- coding: utf-8 -*-

import wx
import sys
import random
from ctypes import CDLL
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
        self.set_icon()
        self.window = Window(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        # self.window.saveScore()
        self.Destroy()

    def set_icon(self):
        icon = wx.Icon("..\images\icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)


class Window(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.buffer = None
        self.bgFont = None
        self.scFont = None
        self.smFont = None
        self.curScore = None
        self.bstScore = None
        self.data = None
        self.colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
                       16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
                       256: (237, 207, 114), 512: (237, 207, 114), 1024: (237, 207, 114), 2048: (237, 207, 114),
                       4096: (237, 207, 114), 8192: (237, 207, 114), 16384: (237, 207, 114), 32768: (237, 207, 114),
                       65536: (237, 207, 114), 131072: (237, 207, 114), 262144: (237, 207, 114),
                       524288: (237, 207, 114), 1048576: (237, 207, 114), 2097152: (237, 207, 114),
                       4194304: (237, 207, 114), 8388608: (237, 207, 114), 16777216: (237, 207, 114),
                       33554432: (237, 207, 114), 67108864: (237, 207, 114), 134217728: (237, 207, 114),
                       268435456: (237, 207, 114), 536870912: (237, 207, 114), 1073741824: (237, 207, 114),
                       2147483648: (237, 207, 114), 4294967296: (237, 207, 114), 8589934592: (237, 207, 114),
                       17179869184: (237, 207, 114), 34359738368: (237, 207, 114), 68719476736: (237, 207, 114),
                       137438953472: (237, 207, 114), 274877906944: (237, 207, 114), 549755813888: (237, 207, 114),
                       1099511627776: (237, 207, 114), 2199023255552: (237, 207, 114), 4398046511104: (237, 207, 114),
                       8796093022208: (237, 207, 114), 17592186044416: (237, 207, 114), 35184372088832: (237, 207, 114),
                       70368744177664: (237, 207, 114), 140737488355328: (237, 207, 114),
                       281474976710656: (237, 207, 114), 562949953421312: (237, 207, 114),
                       1125899906842624: (237, 207, 114), 2251799813685248: (237, 207, 114),
                       4503599627370496: (237, 207, 114), 9007199254740992: (237, 207, 114),
                       18014398509481984: (237, 207, 114), 36028797018963968: (237, 207, 114),
                       72057594037927936: (237, 207, 114)}
        self.init_game()
        self.init_buffer()

        self.Bind(wx.EVT_SIZE, self.on_size)  # use wx.BufferedPaintDC
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def init_buffer(self):
        w, h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w, h)

    def init_game(self):
        self.bgFont = wx.Font(50, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.scFont = wx.Font(36, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.smFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.curScore = 0
        self.bstScore = 0
        # loadScore()
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        count = 0
        while count < 2:
            row = random.randint(0, len(self.data)-1)
            col = random.randint(0, len(self.data[0])-1)
            if self.data[row][col] != 0:
                continue
            if random.randint(0, 1):
                self.data[row][col] = 2
            else:
                self.data[row][col] = 4
            count += 1
        mm = CDLL("mm.dll")

    def on_size(self, event):
        self.init_buffer()
        self.draw_all()

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)

    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_UP:
            # print key_code
            self.do_move(*self.slide_up_down(True))
        elif key_code == wx.WXK_DOWN:
            # print key_code
            self.do_move(*self.slide_up_down(False))
        # elif key_code == wx.WXK_LEFT:
        #     self.do_move(*self.slideLeftRight(True))
        # elif key_code == wx.WXK_RIGHT:
        #     self.do_move(*self.slideLeftRight(False))

    def slide_up_down(self, up):
        score = 0
        num_cols = len(self.data[0])
        num_rows = len(self.data)
        old_data = [[0 for i in range(num_cols)] for j in range(num_rows)]
        for row in range(num_rows):
            for col in range(num_cols):
                old_data[row][col] = self.data[row][col]
        for col in range(num_cols):
            cvl = []
            for row in range(num_rows):
                value = self.data[row][col]
                if value != 0:
                    cvl.append(value)
            if len(cvl) >= 2:
                flags = [True]*len(cvl) #reserve flags
                i = 1
                while i < len(cvl):
                    if cvl[i-1] == cvl[i]:
                        flags[i-1] = False
                        cvl[i] *= 2
                        score += cvl[i]
                        i += 1
                    i += 1
                temp = []
                for i in range(len(cvl)):
                    if flags[i]:
                        temp.append(cvl[i])
                cvl = temp
            for i in range(num_rows-len(cvl)):
                if up:
                    cvl.append(0)
                else:
                    cvl.insert(0, 0)
            for row in range(num_rows):
                self.data[row][col] = cvl[row]
        return old_data != self.data, score

    def do_move(self, move, score):
        if move:
            self.put_tile()
            self.draw_change(score)
            # if self.isGameOver():
            #     if wx.MessageBox("游戏结束，是否重新开始？", "哈哈",wx.YES_NO|wx.ICON_INFORMATION)==wx.YES:
            #         bstScore = self.bstScore
            #         self.initGame()
            #         self.bstScore = bstScore
            #         self.drawAll()

    def put_tile(self):
        available = []
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col] == 0:
                    available.append((row, col))
        if available:
            row, col = available[random.randint(0, len(available)-1)]
            if random.randint(0, 1):
                self.data[row][col] = 2
            else:
                self.data[row][col] = 4
            return True
        return False

    def draw_all(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.draw_bg(dc)
        self.draw_logo(dc)
        self.draw_label(dc)
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
                value = self.data[row][col]
                color = self.colors[value]
                if value == 2 or value == 4:
                    dc.SetTextForeground((119, 110, 101))
                else:
                    dc.SetTextForeground((255, 255, 255))
                dc.SetBrush(wx.Brush(color))
                dc.SetPen(wx.Pen(color))
                dc.DrawRoundedRectangle(30+col*115, 165+row*115, 100, 100, 50)
                size = dc.GetTextExtent(str(value))
                while size[0] > 100-15*2:
                    self.scFont = wx.Font(self.scFont.GetPointSize()*4/5, wx.SWISS, wx.NORMAL, wx.BOLD, face=u"Roboto")
                    dc.SetFont(self.scFont)
                    size = dc.GetTextExtent(str(value))
                if value != 0:
                    dc.DrawText(str(value), 30+col*115+(100-size[0])/2, 165+row*115+(100-size[1])/2)

    def draw_change(self, score):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        if score:
            self.curScore += score
            if self.curScore > self.bstScore:
                self.bstScore = self.curScore
            # self.drawScore(dc)
        self.draw_tiles(dc)

if __name__ == "__main__":
    app = App()
    app.MainLoop()
    # randint = random.randint(0, 1)
    # if randint:
    #     print randint, True
    # else:
    #     print randint, False
