from abc import ABC, abstractmethod
import tkinter as tk


class WindowBase(ABC):
    def __init__(self, root, title, width, height, x_pos=0, y_pos=0, syncronized_windows=[], topmost_flag=False):
        self.window = tk.Toplevel(root)
        self.window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        self.window.title(title)
        self.window.wm_attributes("-topmost", topmost_flag)
        self.window.overrideredirect(True)
        self.observers = []

        # 位置移動を同期させるウィンドウ
        self.syncronized_windows: list[WindowBase] = syncronized_windows
        print(syncronized_windows)

        self.origin = (0, 0)
        self.isMouseDown = False
        self.originText = (0, 0)
        self.isMouseDownText = False

        self.setup_window()

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, event):
        for observer in self.observers:
            observer.update(event)

    @abstractmethod
    def update(self, event):
        raise NotImplementedError("Subclass must implement 'update' method")

    def add_syncronized_window(self, window):
        self.syncronized_windows.append(window)

    def setup_window(self):
        self.window.bind("<Button-1>", self.mouse_down)
        self.window.bind("<ButtonRelease-1>", self.mouse_release)
        self.window.bind("<B1-Motion>", self.mouseMove)
        self.window.bind("<FocusIn>", self.on_focus_in)
        self.window.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, event):
        pass

    def on_focus_out(self, event):
        pass

    def on_click(self, event):

        print(f"{self.window.title()} がクリックされました")

    def mouse_down(self, e):
        if e.num == 1:
            self.origin = (e.x, e.y)
            self.isMouseDown = True

    def mouse_release(self, e):
        self.isMouseDown = False

    def mouseMove(self, e):
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
