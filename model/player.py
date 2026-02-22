import time
from pynput import mouse
from model.action import MouseAction


class Player:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.is_playing = False

    def play_script(self, actions: list[MouseAction]):
        """
        录制模式：按照脚本执行
        """
        self.is_playing = True
        for action in actions:
            if not self.is_playing:
                break

            # 1. 处理延迟
            time.sleep(action.delay)

            # 2. 移动到坐标
            self.mouse_controller.position = (action.x, action.y)

            # 3. 执行点击动作
            # pynput 的 Button 接收字符串名称，如 'left'
            button = mouse.Button[action.button]
            if action.pressed:
                self.mouse_controller.press(button)
            else:
                self.mouse_controller.release(button)

        self.is_playing = False

    def play_fast_click(self, interval: float = 0.01, button_name: str = 'left'):
        """
        连点模式：在当前位置高速连点
        interval: 两次点击之间的间隔
        """
        self.is_playing = True
        button = mouse.Button[button_name]

        while self.is_playing:
            self.mouse_controller.click(button, 1)  # 在当前位置点击 1 次
            time.sleep(interval)

    def stop(self):
        """
        强制停止播放
        """
        self.is_playing = False
