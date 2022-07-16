import sys

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# Создаем приложение
app = QApplication(sys.argv)
clipboard = QApplication.clipboard()

# Обращаемся к буферу обмена
text = clipboard.text()


# Обрабатываем нажатие клавиш
def text_method():
    print("HELLO")


class MainWindow(QWidget):
    def __int__(self):
        super().__init__()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            text_method()

    # Создаем иконку и помещаем ее в системный трей
    trayIcon = QSystemTrayIcon(QIcon('simpless_icon64.png'), parent=app)
    trayIcon.setToolTip('Click on Me!')
    trayIcon.show()

    # Создаем меню
    menu = QMenu()
    exitAction = menu.addAction('Exit')
    exitAction.triggered.connect(app.quit)
    trayIcon.setContextMenu(menu)


# Создаем список с историей буфера обмена
clipboard_history = []

demo = MainWindow()
demo.show()
sys.exit(app.exec())
