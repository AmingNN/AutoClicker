import os
import time
from PySide6.QtCore import QObject, Signal
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
        self.refresh_script_list()  # 启动时自动加载文件

    def _setup_signals(self):
        # 1. 绑定 View 按钮切换模式
        self.view.btn_clicker.clicked.connect(lambda: self._switch_mode("clicker"))
        self.view.btn_script.clicked.connect(lambda: self._switch_mode("script"))

        # 2. 绑定 Controller 信号到 View 的更新方法
        self.status_updated.connect(self.view.update_status)
        self.view.btn_refresh.clicked.connect(self.refresh_script_list)

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

    def refresh_script_list(self):
        """核心逻辑：扫描并显示脚本文件"""
        # 1. 确保目录存在
        if not os.path.exists("records"):
            os.makedirs("records")

        # 2. 获取所有 yaml 文件
        files = [f for f in os.listdir("records") if f.endswith(".yaml")]

        # 3. 清空并重新填充 View 里的列表
        self.view.script_list.clear()
        if not files:
            self.view.script_list.addItem("暂无脚本，请按 F8 录制")
        else:
            # 按照文件修改时间排序，让最新的录制排在前面
            files.sort(key=lambda x: os.path.getmtime(os.path.join("records", x)), reverse=True)
            self.view.script_list.addItems(files)

    def _on_press(self, key):
        if key == keyboard.Key.f8:
            self.toggle_task()
        if key == keyboard.Key.f9:
            self.start_replay()

    def toggle_task(self):
        if self.is_active:
            self.stop_work()
        else:
            self.start_work()

        # 在 Coordinator 类中
    def start_replay(self):
        if self.is_active:
            return

        # 只有在录制模式页面且选中了项目时才播放
        selected_item = self.view.script_list.currentItem()

        # 增加一个判断：如果选中的是“暂无脚本”提示语，则不执行
        if self.current_mode == "script" and selected_item and ".yaml" in selected_item.text():
            from model.action import load_actions_from_yaml
            import threading

            script_path = os.path.join("records", selected_item.text())
            actions = load_actions_from_yaml(script_path)

            if actions:
                self.is_active = True
                self.status_updated.emit(f"Playing: {selected_item.text()}", "#34C759")

                # 开启回放线程
                t = threading.Thread(target=self._run_replay_thread, args=(actions,), daemon=True)
                t.start()

    def _run_replay_thread(self, actions):
        self.player.play_script(actions)
        self.is_active = False
        self.status_updated.emit("Ready", "#1D1D1F")

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
                if not os.path.exists("records"):
                    os.makedirs("records")
                filename = f"records/record_{int(time.time())}.yaml"
                save_actions_to_yaml(actions, filename)
                self.refresh_script_list()

        self.status_updated.emit("Ready", "#1D1D1F")
