import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile, QTextStream, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoClicker")
        self.setFixedSize(380, 500)

        # 1. 设置窗口图标
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "app_icon.png")
        self.setWindowIcon(QIcon(icon_path))

        # 2. 初始化 UI
        self.init_ui()

        # 3. 加载样式 (放在 init_ui 之后确保组件已创建)
        self.load_stylesheet()

    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        file = QFile(qss_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def init_ui(self):
        # 中央部件设置 ID 供 QSS 识别
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 状态显示
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 模式选择区 (放入一个容器里做圆角底色)
        self.mode_container = QWidget()
        self.mode_container.setObjectName("mode_container")
        mode_layout = QVBoxLayout(self.mode_container)

        self.btn_clicker = QPushButton("连点模式")
        self.btn_script = QPushButton("录制模式")
        # 默认点击模式激活 (QSS 中用 [active="true"] 识别)
        self.btn_clicker.setProperty("active", "true")

        mode_layout.addWidget(self.btn_clicker)
        mode_layout.addWidget(self.btn_script)
        layout.addWidget(self.mode_container)

        # 间隔设置区
        self.interval_input = QLineEdit()
        self.interval_input.setPlaceholderText("点击间隔 (秒)... 默认 0.01")
        layout.addWidget(self.interval_input)

        layout.addStretch()  # 弹簧，将内容往上推

        # 热键提示
        self.hint_label = QLabel("Press F8 to Start / Stop")
        self.hint_label.setObjectName("hint_label")
        self.hint_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.hint_label)
