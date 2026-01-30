from PySide6.QtCore import QObject, QThread, Signal
from pynput import keyboard
from model.recorder import Recorder
from model.player import Player


class Coordinator(QObject):
    # 定义一些内部状态信号，方便更新 UI
    status_changed = Signal(str)

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.recorder = Recorder()
        self.player = Player()

        self.is_active = False  # 记录当前是否正在工作（录制或回放）

        # 1. 绑定 UI 按钮（点击界面按钮切换模式等）
        self.setup_connections()

        # 2. 启动全局热键监听
        self.start_hotkey_listener()

    def setup_connections(self):
        # 示例：点击界面上的模式按钮，View 只需要切换显示，Controller 记录状态
        self.view.btn_clicker.clicked.connect(lambda: self.set_mode("clicker"))
        self.view.btn_script.clicked.connect(lambda: self.set_mode("script"))

    def start_hotkey_listener(self):
        # 使用 pynput 监听全局键盘
        self.hotkey_listener = keyboard.Listener(on_press=self._on_key_press)
        self.hotkey_listener.start()

    def _on_key_press(self, key):
        # 检查是否按下 F8
        if key == keyboard.Key.f8:
            self.toggle_work()

    def toggle_work(self):
        """核心切换逻辑：开始或停止"""
        if self.is_active:
            self.stop_all()
        else:
            self.start_all()

    def start_all(self):
        self.is_active = True
        # 根据当前模式，决定是启动 recorder 还是 player
        # 这里需要处理线程逻辑...
        self.status_changed.emit("Running...")

    def stop_all(self):
        self.is_active = False
        self.recorder.stop()
        self.player.stop()
        self.status_changed.emit("Ready")