import sys

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget
from PyQt6.QtGui import QIcon
from pynput import keyboard

# Создаем приложение
app = QApplication(sys.argv)
clipboard = QApplication.clipboard()

# Создаем список с историей буфера обмена
clipboard_history = []

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

# Создаем иконку и помещаем ее в системный трей
trayIcon = QSystemTrayIcon(QIcon('simpless_icon64.png'), parent=app)
trayIcon.setToolTip('Click on Me!')
trayIcon.show()

# Создаем меню
menu = QMenu()
exitAction = menu.addAction('Exit')
exitAction.triggered.connect(app.quit)
trayIcon.setContextMenu(menu)


# Обрабатываем нажатие клавиш
def on_press(key):
    if any([key in comb for comb in COPY_COMBINATIONS]):
        current_copy.add(key)
        if any(all(k in current_copy for k in comb) for comb in COPY_COMBINATIONS):
            current_clipboard_text = clipboard.text()
            f = open("clipboard_history.txt", "a")
            clipboard_history.append(current_clipboard_text)
            f.write(current_clipboard_text + '\n')
            f.close()


def on_release(key):
    if key == keyboard.KeyCode(char='c'):
        print(clipboard_history)
    try:
        current_copy.remove(key)
    except KeyError:
        pass


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    sys.exit(app.exec())
