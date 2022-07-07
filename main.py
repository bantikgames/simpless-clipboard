import sys

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QClipboard

app = QApplication(sys.argv)
clipboard = QClipboard


# Create the icon
trayIcon = QSystemTrayIcon(QIcon('simpless_icon64.png'), parent=app)
trayIcon.setToolTip('Click on Me!')
trayIcon.show()

menu = QMenu()
exitAction = menu.addAction('Exit')
exitAction.triggered.connect(app.quit)

trayIcon.setContextMenu(menu)

sys.exit(app.exec())
