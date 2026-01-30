import os
import time
from PySide6.QtCore import QObject, Signal, Slot
from pynput import keyboard
from model.recorder import Recorder
from model.player import Player
from model.action import save_actions_to_yaml


class Coordinator(QObject):
    # 用于安全地跨线程更新 UI 的信号
    status_updated = Signal(str, str)  # (状态文字, 颜色代码)

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.recorder = Recorder()
        self.player = Player()

        self.current_mode = "clicker"  # 默认模式
        self.is_active = False

        self._setup_signals()
        self._start_hotkey_listener()

    def _setup_signals(self):
        # 1. 绑定 View 按钮切换模式
        self.view.btn_clicker.clicked.connect(lambda: self._switch_mode("clicker"))
        self.view.btn_script.clicked.connect(lambda: self._switch_mode("script"))

        # 2. 绑定 Controller 信号到 View 的更新方法
        self.status_updated.connect(self.view.update_status)

    def _switch_mode(self, mode):
        if not self.is_active:
            self.current_mode = mode
            # 更新 View 的按钮状态（通过属性改变 QSS 样式）
            self.view.btn_clicker.setProperty("active", "true" if mode == "clicker" else "false")
            self.view.btn_script.setProperty("active", "true" if mode == "script" else "false")
            self.view.refresh_style()  # 通知 View 刷新样式

    def _start_hotkey_listener(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def _on_press(self, key):
        if key == keyboard.Key.f8:
            self.toggle_task()

    def toggle_task(self):
        if self.is_active:
            self.stop_work()
        else:
            self.start_work()

    def start_work(self):
        self.is_active = True
        if self.current_mode == "clicker":
            self.status_updated.emit("Clicking...", "#007AFF")
            # 开启连点逻辑（实际开发中建议放入 QThread，此处先示意逻辑）
            interval = float(self.view.interval_input.text() or 0.01)
            # 注意：play_fast_click 内部有 while 循环，这里需要异步处理
            import threading
            threading.Thread(target=self.player.play_fast_click, args=(interval,), daemon=True).start()
        else:
            self.status_updated.emit("Recording...", "#FF3B30")  # 苹果红
            self.recorder.start()

    def stop_work(self):
        self.is_active = False
        if self.current_mode == "clicker":
            self.player.stop()
        else:
            actions = self.recorder.stop()
            if actions:
                # 自动保存到 records 文件夹，以时间戳命名
                if not os.path.exists("records"): os.makedirs("records")
                filename = f"records/record_{int(time.time())}.yaml"
                save_actions_to_yaml(actions, filename)

        self.status_updated.emit("Ready", "#1D1D1F")

