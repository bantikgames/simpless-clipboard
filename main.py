import sys
from PyQt6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QListWidget,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton)
from PyQt6.QtGui import QIcon, QClipboard
from pynput import keyboard

# Создаем основное приложение

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

clipboard = QApplication.clipboard()

# Комбинации горячих клавиш
COPY_COMBINATIONS = [
    {keyboard.Key.ctrl_l, keyboard.KeyCode(char='c')},
    {keyboard.Key.ctrl_r, keyboard.KeyCode(char='c')}
]

# Текущие нажатые клавиши
current_copy = set()


class ListWidget(QListWidget):
    def __init__(self):
        super(ListWidget, self).__init__()
        self.setUniformItemSizes(True)

    def mouseDoubleClickEvent(self, event):
        show_tray_message(trayIcon, "Текст скопирован в буфер обмена", self.currentItem().text())
        clipboard.setText(self.currentItem().text())


widget_list = ListWidget()


def click_on_button():
    with open("clipboard_history.txt", "r+") as file:
        file.truncate(0)
    widget_list.clear()


def copy_text():
    current_clipboard_text = clipboard.text(mode=QClipboard.Mode.Selection)
    if current_clipboard_text and not current_clipboard_text.isspace():
        with open("clipboard_history.txt", "r+") as file:
            file.write(current_clipboard_text.strip() + '\n')
            widget_list.addItem(current_clipboard_text.strip())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Simpless Clipboard")
        self.setWindowIcon(QIcon('simpless_icon64.png'))

        btn_clear = QPushButton("Очистить историю буфера обмена")
        btn_clear.pressed.connect(click_on_button)

        layout = QVBoxLayout()
        layout.addWidget(widget_list)
        layout.addWidget(btn_clear)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        clipboard.dataChanged.connect(copy_text)


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


# Обрабатываем нажатие и отпускание клавиш копирования и вставки
def on_press(key):
    if any([key in comb for comb in COPY_COMBINATIONS]):
        current_copy.add(key)
        if any(all(k in current_copy for k in comb) for comb in COPY_COMBINATIONS):
            copy_text()


def on_release(key):
    try:
        current_copy.remove(key)
    except KeyError:
        pass


if __name__ == '__main__':
    load_clipboard_history()
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()
    sys.exit(app.exec())
