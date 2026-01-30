import time
from pynput import mouse
from model.action import MouseAction


class Recorder:
    def __init__(self):
        self.actions = []
        self.last_time = None
        self.listener = None
        self.is_recording = False

    def _get_delay(self):
        """计算距离上一个动作的时间间隔"""
        now = time.time()
        if self.last_time is None:
            delay = 0.0
        else:
            delay = now - self.last_time
        self.last_time = now
        return round(delay, 4)  # 保留四位小数，足够精确且简洁

    def _on_click(self, x, y, button, pressed):
        """鼠标点击回调"""
        if not self.is_recording:
            return False  # 停止监听

        # 创建动作模型
        action = MouseAction(
            action_type='click',
            delay=self._get_delay(),
            x=int(x),
            y=int(y),
            button=button.name,  # 'left' or 'right'
            pressed=pressed
        )
        self.actions.append(action)

    def start(self):
        """开始录制"""
        self.actions = []
        self.last_time = time.time()
        self.is_recording = True

        # 启动监听器
        self.listener = mouse.Listener(on_click=self._on_click)
        self.listener.start()
        print("Model: Recording started...")

    def stop(self):
        """停止录制并返回动作列表"""
        self.is_recording = False
        if self.listener:
            self.listener.stop()
        print(f"Model: Recording stopped. Captured {len(self.actions)} actions.")
        return self.actions
