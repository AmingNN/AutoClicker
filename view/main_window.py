import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, \
    QListWidget, QHBoxLayout, QStackedWidget
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
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 1. 状态显示
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 2. 模式选择按钮 (这部分是公共的)
        self.mode_container = QWidget()
        self.mode_container.setObjectName("mode_container")
        mode_btn_layout = QHBoxLayout(self.mode_container)  # 改为横向排布更像苹果风格

        self.btn_clicker = QPushButton("连点模式")
        self.btn_script = QPushButton("录制模式")
        self.btn_clicker.setProperty("active", "true")

        mode_btn_layout.addWidget(self.btn_clicker)
        mode_btn_layout.addWidget(self.btn_script)
        layout.addWidget(self.mode_container)

        # --- 3. 核心：堆栈容器 (QStackedWidget) ---
        self.pages = QStackedWidget()
        layout.addWidget(self.pages)

        # [第一页：连点模式页面]
        self.clicker_page = QWidget()
        clicker_layout = QVBoxLayout(self.clicker_page)
        self.interval_input = QLineEdit()
        self.interval_input.setPlaceholderText("点击间隔 (秒)... 默认 0.01")
        clicker_layout.addWidget(QLabel("设置点击频率:"))
        clicker_layout.addWidget(self.interval_input)
        clicker_layout.addStretch()  # 推到顶部
        self.pages.addWidget(self.clicker_page)

        # [第二页：录制模式页面]
        self.script_page = QWidget()
        script_layout = QVBoxLayout(self.script_page)

        # 列表头
        list_header = QHBoxLayout()
        list_header.addWidget(QLabel("已录制脚本"))
        self.btn_refresh = QPushButton("刷新")
        self.btn_refresh.setObjectName("refresh_btn")
        self.btn_refresh.setFixedWidth(60)
        list_header.addStretch()
        list_header.addWidget(self.btn_refresh)
        script_layout.addLayout(list_header)

        # 脚本列表
        self.script_list = QListWidget()
        self.script_list.setObjectName("script_list")
        script_layout.addWidget(self.script_list)
        self.pages.addWidget(self.script_page)

        # --- 4. 底部提示 ---
        layout.addStretch()
        self.hint_label = QLabel("F8: 开始/停止 | F9: 回放选中")
        self.hint_label.setObjectName("hint_label")
        self.hint_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.hint_label)

        # 5. 绑定切换逻辑 (这是 View 内部的视觉切换)
        self.btn_clicker.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btn_script.clicked.connect(lambda: self.pages.setCurrentIndex(1))

    def update_status(self, text, color):
        """更新状态文字和颜色"""
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: 700;")

    def refresh_style(self):
        """刷新样式，使按钮的 active 属性生效"""
        self.style().unpolish(self.btn_clicker)
        self.style().polish(self.btn_clicker)
        self.style().unpolish(self.btn_script)
        self.style().polish(self.btn_script)
        self.update()
