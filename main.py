import sys
from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.coordinator import Coordinator


def main():
    app = QApplication(sys.argv)

    # 实例化 View
    view = MainWindow()

    # 实例化 Controller，并将 View 注入进去
    # 这一步完成了 MVC 的闭环
    controller = Coordinator(view)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
