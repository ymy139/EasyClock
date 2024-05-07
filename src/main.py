from threading import Thread
from sys import argv, exit
from time import strftime
from os import chdir
from os.path import split, normpath

from PyQt6.QtWidgets import QApplication

from models import Funcs, Windows

chdir(normpath(split(__file__)[0]+"\\.."))

app = QApplication(argv)
window = Windows.MainWindow()
slots = Windows.Slots(window)

window.greeting.setText(Funcs.getGreetingSentence(int(strftime("%H"))))
slots.ChangeAnotherSentence()

window.anotherSentence.clicked.connect(slots.ChangeAnotherSentence)
window.toDoList_add.clicked.connect(slots.addToDoItem)
window.toDoList_del.clicked.connect(slots.delToDoItem)

updataWindowThread = Thread(target=slots.updataWindow, daemon=True)
updataWindowThread.start()

window.show()
exit(app.exec())