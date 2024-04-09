from threading import Thread
from sys import argv, exit
from time import sleep, strftime
from os import chdir
from os.path import split, normpath

from PyQt6.QtWidgets import QApplication, QListWidgetItem
from PyQt6.QtCore import Qt

from models import Funcs, Windows

chdir(normpath(split(__file__)[0]+"\\.."))

def updataWindow() -> None:
    try:
        while True:
            nowTime = Funcs.getNowTime()
            lunarDay = Funcs.solarToLunar(int(strftime("%Y")), 
                                        int(strftime("%m")), 
                                        int(strftime("%d")))
            
            window.timeWidget["hour"].setText(nowTime["hour"])
            window.timeWidget["minute"].setText(nowTime["minute"])
            window.timeWidget["second"].setText(nowTime["second"])
            
            window.date.setText(strftime("%Y年%m月%d日")+" "+
                                nowTime["weekday"]+" "+
                                Funcs.getLunarDateString(lunarDay[1], lunarDay[2]))
            
            window.countdown.setText("高考倒计时："+str(Funcs.calculateCountdown(6, 7))+"天")
            
            QApplication.processEvents()
            sleep(0.2)
    except: pass

def ChangeAnotherSentence() -> None:
    sentence = Funcs.getASentence()
    window.sentence.setText("「"+sentence["sentence"]+"」")
    if sentence["from"] != None and sentence["from_who"] == None:
        window.sentenceFrom.setText("——「"+sentence["from"]+"」")
    elif sentence["from"] == None and sentence["from_who"] != None:
        window.sentenceFrom.setText("——"+sentence["from_who"])
    else:
        window.sentenceFrom.setText("——"+sentence["from_who"]+"「"+sentence["from"]+"」")
        
def addToDoItem() -> None:
    newItem = QListWidgetItem(window.toDoList)
    newItem.setText("新建待办事项")
    newItem.setFlags(Qt.ItemFlag.ItemIsEditable | 
                     Qt.ItemFlag.ItemIsSelectable | 
                     Qt.ItemFlag.ItemIsDragEnabled | 
                     Qt.ItemFlag.ItemIsUserCheckable | 
                     Qt.ItemFlag.ItemIsEnabled)

def delToDoItem() -> None:
    currentItem = window.toDoList.currentItem()
    if currentItem != None:
        row = window.toDoList.row(currentItem)
        window.toDoList.takeItem(row)

app = QApplication(argv)
window = Windows.MainWindow()

window.greeting.setText(Funcs.getGreetingSentence(int(strftime("%H"))))
ChangeAnotherSentence()

window.anotherSentence.clicked.connect(ChangeAnotherSentence)
window.toDoList_add.clicked.connect(addToDoItem)
window.toDoList_del.clicked.connect(delToDoItem)

updataWindowThread = Thread(target=updataWindow, daemon=True)
updataWindowThread.start()

window.show()
exit(app.exec())