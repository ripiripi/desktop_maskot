from abc import ABC, abstractmethod
import tkinter as tk
from .enum import Event


class WindowBase(ABC):
    def __init__(self, root, title, width, height, x_pos=0, y_pos=0, syncronized_windows=[], topmost_flag=False):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        self.title = title
        self.window.title(title)
        self.window.wm_attributes("-topmost", topmost_flag)
        self.window.overrideredirect(True)
        self.current_alpha = 1.0
        self.observers = []
        self.relative_pos = []
        self.syncronized_windows = []
        self.origin = (0, 0)
        self.originText = (0, 0)
        self.isMouseDown = False
        self.isMouseDownText = False
        self.translucent = False

        self.add_syncronized_window(syncronized_windows)
        self.setup_window()

    def add_observer(self, observers: list):
        for observer in observers:
            self.observers.append(observer)

    def notify_observers(self, event):
        for observer in self.observers:
            observer.update(event)

    def update(self, event):
        if event == Event.TRUNSLUCENT:
            self.turn_translucent()

    def add_syncronized_window(self, window_list: list):
        # メインウィンドウの位置を取得
        main_geom = self.window.geometry().split("+")
        main_x, main_y = int(main_geom[1]), int(main_geom[2])
        for window in window_list:
            self.syncronized_windows.append(window)
            # サブウィンドウの位置を取得
            sub_geom = window.window.geometry().split("+")
            sub_x, sub_y = int(sub_geom[1]), int(sub_geom[2])
            # 相対位置を計算して保存
            self.relative_pos.append((sub_x - main_x, sub_y - main_y))

    def setup_window(self):
        self.window.bind("<Button-1>", self.mouse_down)
        self.window.bind("<Double-1>", self.mouse_double_click)
        self.window.bind("<Button-3>", self.mouse_right_down)
        self.window.bind("<ButtonRelease-1>", self.mouse_release)
        self.window.bind("<B1-Motion>", self.mouse_move)
        self.window.bind("<FocusIn>", self.on_focus_in)
        self.window.bind("<FocusOut>", self.on_focus_out)
        self.window.bind("<Enter>", self.on_mouse_enter)
        self.window.bind("<Leave>", self.on_mouse_leave)

    def mouse_double_click(self, event):
        pass

    def mouse_right_down(self, event):
        self.notify_observers(Event.TRUNSLUCENT)
        self.turn_translucent()

    def turn_translucent(self):
        if self.current_alpha == 0:  # 透明度が0の場合は何もしない
            return
        if self.translucent:
            self.window.attributes("-alpha", 1.0)
            self.current_alpha = 1.0
            self.translucent = False
        else:
            self.window.attributes("-alpha", 0.5)
            self.current_alpha = 0.5
            self.translucent = True

    def on_mouse_enter(self, event):
        pass

    def on_mouse_leave(self, event):
        pass

    def on_focus_in(self, event):
        pass

    def on_focus_out(self, event):
        pass

    def on_click(self, event):
        pass

    def mouse_down(self, e):
        if e.num == 1:
            self.origin = (e.x, e.y)
            self.isMouseDown = True

    def mouse_release(self, e):
        self.isMouseDown = False

    def mouse_move(self, e):
        if self.isMouseDown:
            buf = self.window.geometry().split("+")
            self.setPos(
                e.x - self.origin[0] + int(buf[1]),
                e.y - self.origin[1] + int(buf[2]),
            )
            self.syncSubWindow(e.x - self.origin[0], e.y - self.origin[1])

    def syncSubWindow(self, dx, dy):
        # sub_window: WindowBase
        for sub_window in self.syncronized_windows:
            buf = sub_window.window.geometry().split("+")
            current_x = int(buf[1])
            current_y = int(buf[2])

            new_x = current_x + dx
            new_y = current_y + dy
            sub_window.setPos(new_x, new_y)

    def mouseDownText(self, e):
        if e.num == 1:
            self.originText = (e.x, e.y)
            self.isMouseDownText = True

    def mouseReleaseText(self, e):
        self.isMouseDownText = False

    def setPos(self, x, y):
        self.window.geometry("+%s+%s" % (x, y))
