from threading import Thread
from sys import argv, exit
from time import strftime
from os import chdir
from os.path import split, normpath

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from models import Funcs, Settings, Windows

chdir(normpath(split(__file__)[0]+"\\.."))

settings = Settings.readSettings()

app = QApplication(argv)
if settings["window"]["alwaysOnTop"] == True: # type: ignore
    window = Windows.MainWindow(Qt.WindowType.WindowStaysOnTopHint)
else:
    window = Windows.MainWindow()
slots = Windows.Slots(window)

window.greeting.setText(Funcs.getGreetingSentence(int(strftime("%H"))))
slots.ChangeAnotherSentence()

window.anotherSentence.clicked.connect(slots.ChangeAnotherSentence)
window.toDoList_add.clicked.connect(slots.addToDoItem)
window.toDoList_del.clicked.connect(slots.delToDoItem)

updataWindowThread = Thread(target=slots.updataWindowLoop, daemon=True)
updataWindowThread.start()

window.show()
exit(app.exec())