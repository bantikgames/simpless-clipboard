import sys

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QListWidget
from PyQt6.QtGui import QIcon
from pynput import keyboard

# Создаем основное приложение
app = QApplication(sys.argv)
clipboard = QApplication.clipboard()
app.setQuitOnLastWindowClosed(False)
app.setApplicationName("Simpless Clipboard")
app.setWindowIcon(QIcon('simpless_icon64.png'))


class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.setUniformItemSizes(True)

    def windowTitle(self):
        return "Simpless Clipboard"

    def mouseDoubleClickEvent(self, event):
        clipboard.setText(self.currentItem().text())


widget_list = ListWidget()

# Создаем меню для основного приложения и виджета
menu = QMenu()
showAction = menu.addAction("Показать")
showAction.triggered.connect(widget_list.show)
hideAction = menu.addAction('Скрыть')
hideAction.triggered.connect(widget_list.hide)
exitAction = menu.addAction("Закрыть")
exitAction.triggered.connect(app.quit)

# Создаем иконку и помещаем ее в системный трей
trayIcon = QSystemTrayIcon(QIcon('simpless_icon64.png'), parent=widget_list)
trayIcon.setToolTip('Кликнуть ПКМ, чтобы открыть настройки')
trayIcon.show()
trayIcon.setContextMenu(menu)

# Создаем список с историей буфера обмена и задаем его максимальный объем
clipboard_history = []
max_clipboard_count = 50

# Комбинации горячих клавиш
COPY_COMBINATIONS = [
    {keyboard.Key.ctrl_l, keyboard.KeyCode(char='c')},
    {keyboard.Key.ctrl_r, keyboard.KeyCode(char='c')}
]

PASTE_COMBINATIONS = [
    {keyboard.Key.ctrl_l, keyboard.KeyCode(char='u')},
    {keyboard.Key.ctrl_r, keyboard.KeyCode(char='u')}
]

# Текущие нажатые клавиши
current_copy = set()
current_paste = set()


# Обрабатываем нажатие и отпускание клавиш копирования и вставки
def on_press(key):
    if any([key in comb for comb in COPY_COMBINATIONS]):
        current_copy.add(key)
        if any(all(k in current_copy for k in comb) for comb in COPY_COMBINATIONS):
            current_clipboard_text = clipboard.text()
            clipboard_history.append(current_clipboard_text)
            if current_clipboard_text and not current_clipboard_text.isspace():
                with open("clipboard_history.txt", "r+") as file:
                    count = 1
                    for _ in file:
                        count += 1
                    file.write(current_clipboard_text.strip() + '\n')
                    widget_list.addItem(current_clipboard_text.strip())
                    print(
                        f'Элемент {current_clipboard_text.strip()} добавлен в историю буфера обмена. Всего в буфере {count} записей')
            else:
                print("Строка пустая")


def load_clipboard_history():
    with open("clipboard_history.txt", "r+") as file:
        for i in file:
            widget_list.addItem(i.strip())


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
