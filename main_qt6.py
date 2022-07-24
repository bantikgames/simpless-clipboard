import keyboard
import pyperclip
import sys
import time

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QListWidget,
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout, QLabel, QCheckBox, QSpacerItem, QSizePolicy)

# Создаем основное приложение и доступ к буферу обмена


clipboard = pyperclip


class MainWindow(QMainWindow):
    tray_icon = None
    check_box = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Simpless Clipboard")
        self.setWindowIcon(QIcon('simpless_icon64.png'))

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QGridLayout(self)
        widget.setLayout(layout)
        layout.addWidget(
            QLabel("Приложение может быть свернуто при закрытии в трей", self), 0, 0)

        self.check_box = QCheckBox('Свернуть в трей')
        layout.addWidget(self.check_box, 1, 0)
        layout.addItem(QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding), 2, 0)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon = QSystemTrayIcon(QIcon('simpless_icon64.png'), parent=self)
        self.tray_icon.setToolTip('Кликнуть ПКМ, чтобы открыть настройки')

        show_action = QAction("Показать", self)
        quit_action = QAction("Выход", self)
        hide_action = QAction("Скрыть", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QApplication.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        btn_clear = QPushButton("Очистить историю буфера обмена")
        btn_clear.pressed.connect(self.clean_clipboard_history)
        layout.addWidget(btn_clear)

        self.widget_list = QListWidget()
        self.widget_list.setUniformItemSizes(True)
        layout.addWidget(self.widget_list)

    def closeEvent(self, event):
        if self.check_box.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Simpless Clipboard",
                "Приложение свернуто в трей",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

    def clean_clipboard_history(self):
        with open("clipboard_history.txt", "r+") as file:
            file.truncate(0)
        self.widget_list.clear()

    def mouseDoubleClickEvent(self, event):
        self.show_tray_message(self.tray_icon, "Текст скопирован в буфер обмена")
        clipboard.copy(self.widget_list.currentItem().text())

    def load_clipboard_history(self):
        with open("clipboard_history.txt", "r+") as file:
            for i in file:
                self.widget_list.addItem(i.strip())

    def show_tray_message(self: QSystemTrayIcon, notification_title, notification_message):
        icon = QIcon('simpless_icon64.png')
        duration = 3 * 1000
        self.showMessage(notification_title, notification_message, icon, duration)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setQuitOnLastWindowClosed(False)
    main_window = MainWindow()
    main_window.show()
    main_window.load_clipboard_history()


    def keyboard_pressed(event):
        if keyboard.is_pressed('ctrl'):
            time.sleep(0.2)
            current_clipboard_text = clipboard.paste()
            if current_clipboard_text and not current_clipboard_text.isspace():
                with open("clipboard_history.txt", "a") as file:
                    file.write(current_clipboard_text.strip() + '\n')
                    main_window.widget_list.addItem(current_clipboard_text.strip())


    keyboard.on_press_key('c', keyboard_pressed)

    sys.exit(app.exec())
