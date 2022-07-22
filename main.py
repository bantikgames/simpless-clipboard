import keyboard
import pyperclip
import sys
import time

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QListWidget,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton)

# Создаем основное приложение и доступ к буферу обмена
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

clipboard = pyperclip


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Simpless Clipboard")
        self.setWindowIcon(QIcon('simpless_icon64.png'))

        btn_clear = QPushButton("Очистить историю буфера обмена")
        btn_clear.pressed.connect(self.clean_clipboard_history)

        layout = QVBoxLayout()
        layout.addWidget(widget_list)
        layout.addWidget(btn_clear)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def clean_clipboard_history(self):
        with open("clipboard_history.txt", "r+") as file:
            file.truncate(0)
        widget_list.clear()


class ListWidget(QListWidget):
    def __init__(self):
        super(ListWidget, self).__init__()
        self.setUniformItemSizes(True)

    def mouseDoubleClickEvent(self, event):
        show_tray_message(trayIcon, "Текст скопирован в буфер обмена", self.currentItem().text())
        clipboard.copy(self.currentItem().text())


widget_list = ListWidget()
main_window = MainWindow()

# Создаем меню для основного приложения и виджета
menu = QMenu()
showAction = menu.addAction("Показать")
showAction.triggered.connect(main_window.show)
hideAction = menu.addAction('Скрыть')
hideAction.triggered.connect(main_window.hide)
exitAction = menu.addAction("Закрыть")
exitAction.triggered.connect(app.quit)

# Создаем иконку и помещаем ее в системный трей
trayIcon = QSystemTrayIcon(QIcon('simpless_icon64.png'), parent=main_window)
trayIcon.setToolTip('Кликнуть ПКМ, чтобы открыть настройки')
trayIcon.show()
trayIcon.setContextMenu(menu)


def show_tray_message(tray: QSystemTrayIcon, notification_title, notification_message):
    icon = QIcon('simpless_icon64.png')
    duration = 3 * 1000
    tray.showMessage(notification_title, notification_message, icon, duration)


def load_clipboard_history():
    with open("clipboard_history.txt", "r+") as file:
        for i in file:
            widget_list.addItem(i.strip())


def keyboard_pressed(event):
    if keyboard.is_pressed('ctrl'):
        time.sleep(0.2)
        current_clipboard_text = clipboard.paste()
        if current_clipboard_text and not current_clipboard_text.isspace():
            with open("clipboard_history.txt", "a") as file:
                file.write(current_clipboard_text.strip() + '\n')
                widget_list.addItem(current_clipboard_text.strip())


if __name__ == '__main__':
    keyboard.on_press_key('c', keyboard_pressed)
    load_clipboard_history()
    sys.exit(app.exec())
