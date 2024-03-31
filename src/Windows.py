from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QListWidget, QApplication

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.loadFonts()
        self.initWindow()
        self.initUIWidget()
        self.initUITexts()
        self.initUIStyleSheets()
        self.about.clicked.connect(self.showAbout)
        
    def loadFonts(self) -> None:
        fontID_ui = QFontDatabase.addApplicationFont("resources/fonts/ui.ttf")
        fontID_time = QFontDatabase.addApplicationFont("resources/fonts/time.ttf")
        self.fontsName = {
            "ui": QFontDatabase.applicationFontFamilies(fontID_ui)[0],
            "time": QFontDatabase.applicationFontFamilies(fontID_time)[0]
        }
        
    def initWindow(self) -> None:
        self.resize(640, 290)
        self.setFont(QFont(self.fontsName["ui"], 12))
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setWindowTitle("EasyClock")
        self.setWindowIcon(QIcon("resources/imgs/icon.ico"))
        
    def initUIWidget(self) -> None:
        self.separators = {
            "time--greeting": QLabel(self),
            "greeting--oneSentence": QLabel(self),
            "left--right": QLabel(self),
            "toDoList--menuBar": QLabel(self)
        }
        
        # left-top: time part
        # ====================================================================
        self.timeWidget = {
            "hour": QLabel(self),
            "minute": QLabel(self),
            "second": QLabel(self)
        }
        
        self.timeWidget["hour"].setGeometry(0, 0, 145, 130)
        self.timeWidget["hour"].setFont(QFont(self.fontsName["time"], 100))
        self.timeWidget["hour"].setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.timeWidget["minute"].setGeometry(150, 0, 145, 130)
        self.timeWidget["minute"].setFont(QFont(self.fontsName["time"], 100))
        self.timeWidget["minute"].setStyleSheet("color: rgb(245, 139, 46);")
        self.timeWidget["minute"].setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.timeWidget["second"].setGeometry(295, 85, 40, 30)
        self.timeWidget["second"].setFont(QFont(self.fontsName["time"], 27))
        self.timeWidget["second"].setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.date = QLabel(self)
        self.date.setGeometry(5, 120, 330, 15)
        self.date.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.countdown = QLabel(self)
        self.countdown.setGeometry(5, 140, 330, 15)
        self.countdown.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # ====================================================================
        
        self.separators["time--greeting"].setGeometry(0, 160, 340, 2)
        
        # left-middle: greeting part
        # ====================================================================
        self.greeting = QLabel(self)
        self.greeting.setGeometry(2, 165, 330, 45)
        self.greeting.setWordWrap(True)
        # ====================================================================
        
        self.separators["greeting--oneSentence"].setGeometry(0, 215, 340, 2)
        
        # left-down: one sentence part
        # ====================================================================
        self.sentence = QLabel(self)
        self.sentence.setGeometry(5, 220, 330, 40)
        self.sentence.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.sentence.setWordWrap(True)
        
        self.sentenceFrom = QLabel(self)
        self.sentence.setGeometry(5, 265, 330, 20)
        self.sentence.setAlignment(Qt.AlignmentFlag.AlignRight)
        # ====================================================================
        
        self.separators["left--right"].setGeometry(340, 0, 2, 290)
        
        # right-top: to do list
        # ====================================================================
        self.toDoListTitle = QLabel(self)
        self.toDoListTitle.setGeometry(345, 0, 70, 30)
        
        self.toDoList_del = QPushButton(self)
        self.toDoList_del.setGeometry(565, 0, 35, 30)
        
        self.toDoList_add = QPushButton(self)
        self.toDoList_add.setGeometry(600, 0, 35, 30)
        
        self.toDoList = QListWidget(self)
        self.toDoList.setGeometry(345, 30, 290, 215)
        # ====================================================================
        
        self.separators["toDoList--menuBar"].setGeometry(340, 250, 300, 2)
        
        # right-down: menu bar
        # ====================================================================
        self.anotherSentence = QPushButton(self)
        self.anotherSentence.setGeometry(345, 255, 90, 30)
        
        self.about = QPushButton(self)
        self.about.setGeometry(575, 255, 60, 30)
        # ====================================================================
        
    def initUITexts(self) -> None:
        self.toDoListTitle.setText("待办列表")
        self.toDoList_del.setText("-")
        self.toDoList_add.setText("+")
        self.anotherSentence.setText("←换一句")
        self.about.setText("关于")
        
    def initUIStyleSheets(self) -> None:
        self.styleSheets = {
            "QPushButton": open("resources/css/QPushButton.css").read(),
            "QListWidget": open("resources/css/QListWidget.css").read()
        }
        
        self.toDoList_del.setStyleSheet(self.styleSheets["QPushButton"])
        self.toDoList_add.setStyleSheet(self.styleSheets["QPushButton"])
        self.toDoList.setStyleSheet(self.styleSheets["QListWidget"])
        self.anotherSentence.setStyleSheet(self.styleSheets["QPushButton"])
        self.about.setStyleSheet(self.styleSheets["QPushButton"])
        
        self.separators["time--greeting"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["greeting--oneSentence"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["left--right"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["toDoList--menuBar"].setStyleSheet("background-color: rgb(160, 160, 160);")
        
    def showAbout(self) -> None:
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()
        
class AboutWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.loadFonts()
        self.initWindow()
        self.initUIWidget()
        self.initUITexts()
        self.ok.clicked.connect(self.close)
        
    def loadFonts(self) -> None:
        fontID_ui = QFontDatabase.addApplicationFont("resources/fonts/ui.ttf")
        self.fontName = QFontDatabase.applicationFontFamilies(fontID_ui)[0]
        
    def initWindow(self) -> None:
        self.resize(385, 130)
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setWindowTitle("EasyClock - 关于")
        self.setWindowIcon(QIcon("resources/imgs/icon.ico"))
        
    def initUIWidget(self) -> None: 
        self.icon = QLabel(self)
        self.icon.setGeometry(0, 0, 100, 100)
        self.icon.setScaledContents(True)
        self.icon.setPixmap(QPixmap("resources/imgs/icon.ico"))
        
        self.title = QLabel(self)
        self.title.setGeometry(110, 0, 270, 40)
        self.title.setFont(QFont(self.fontName, 19))
        
        self.data = QLabel(self)
        self.data.setGeometry(110, 35, 270, 60)
        self.data.setFont(QFont(self.fontName, 10))
        
        self.sentenceFrom = QLabel(self)
        self.sentenceFrom.setGeometry(10, 95, 125, 15)
        self.sentenceFrom.setFont(QFont(self.fontName, 9))
        self.sentenceFrom.setOpenExternalLinks(True)
        
        self.githubRepo = QLabel(self)
        self.githubRepo.setGeometry(10, 110, 250, 15)
        self.githubRepo.setFont(QFont(self.fontName, 9))
        self.githubRepo.setOpenExternalLinks(True)
        
        self.ok = QPushButton(self)
        self.ok.setGeometry(260, 95, 120, 30)
        self.ok.setStyleSheet(open("resources/css/QPushButton.css").read())
        self.ok.setFont(QFont(self.fontName, 11))
    
    def initUITexts(self) -> None:
        self.title.setText("EasyClock 简易学习时钟")
        self.data.setText("Code by: ymy139(余沐垚)\n本软件遵循MIT开源许可证\n使用 Python3.11.6 + PyQt6.6.1 制作")
        self.sentenceFrom.setText("一言来源: <a href='http://hitokoto.cn'>hitokoto.cn</a>")
        self.githubRepo.setText("GitHub仓库: <a href='http://gitHub.com/ymy139/EasyClock'>gitHub.com/ymy139/EasyClock</a>")
        self.ok.setText("确认")
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # win = MainWindow()
    win = AboutWindow()
    win.show()
    exit(app.exec())