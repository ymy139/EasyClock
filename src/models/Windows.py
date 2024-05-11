from time import strftime, sleep

from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QListWidgetItem, QFileDialog, QMessageBox
from qfluentwidgets import PushButton, ListWidget, LineEdit, CheckBox, FluentIcon, ToolButton

from . import Funcs

class MainWindow(QWidget):
    def __init__(self, flags: Qt.WindowType | None = None) -> None:
        if flags != None:
            super().__init__(flags=flags)
        else:
            super().__init__()
        self.loadFonts()
        self.initWindow()
        self.initUIWidget()
        self.initUITexts()
        self.initUIStyleSheets()
        self.settings.clicked.connect(self.showSettings)
        
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
        self.setMaximumSize(640, 290)
        self.setMinimumSize(640, 290)
        
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
        self.timeWidget["hour"].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        self.timeWidget["minute"].setGeometry(150, 0, 145, 130)
        self.timeWidget["minute"].setFont(QFont(self.fontsName["time"], 100))
        self.timeWidget["minute"].setStyleSheet("color: rgb(245, 139, 46);")
        self.timeWidget["minute"].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        self.timeWidget["second"].setGeometry(295, 85, 40, 30)
        self.timeWidget["second"].setFont(QFont(self.fontsName["time"], 27))
        self.timeWidget["second"].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
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
        self.greeting.setGeometry(5, 165, 330, 45)
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
        self.sentenceFrom.setGeometry(5, 265, 330, 20)
        self.sentenceFrom.setAlignment(Qt.AlignmentFlag.AlignRight)
        # ====================================================================
        
        self.separators["left--right"].setGeometry(340, 0, 2, 290)
        
        # right-top: to do list
        # ====================================================================
        self.toDoListTitle = QLabel(self)
        self.toDoListTitle.setGeometry(345, 0, 70, 30)
        
        self.toDoList_del = PushButton(self)
        self.toDoList_del.setGeometry(565, 0, 35, 30)
        
        self.toDoList_add = PushButton(self)
        self.toDoList_add.setGeometry(600, 0, 35, 30)
        
        self.toDoList = ListWidget(self)
        self.toDoList.setGeometry(345, 30, 290, 215)
        self.toDoList.setStyleSheet(open("resources/css/ListWidget.css").read())
        self.toDoList.setWordWrap(True)
        # ====================================================================
        
        self.separators["toDoList--menuBar"].setGeometry(340, 250, 300, 2)
        
        # right-down: menu bar
        # ====================================================================
        self.anotherSentence = PushButton(self)
        self.anotherSentence.setGeometry(345, 255, 90, 30)
        
        self.settings = PushButton(self)
        self.settings.setGeometry(575, 255, 60, 30)
        # ====================================================================
        
    def initUITexts(self) -> None:
        self.toDoListTitle.setText("待办列表")
        self.toDoList_del.setText("-")
        self.toDoList_add.setText("+")
        self.anotherSentence.setText("←换一句")
        self.settings.setText("设置")
        
    def initUIStyleSheets(self) -> None:
        self.separators["time--greeting"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["greeting--oneSentence"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["left--right"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["toDoList--menuBar"].setStyleSheet("background-color: rgb(160, 160, 160);")
        
    def showSettings(self) -> None:
        self.settingsWindow = SettingsWindow()
        self.settingsWindow.show()
        
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
        
        self.ok = PushButton(self)
        self.ok.setGeometry(260, 95, 120, 30)
        self.ok.setFont(QFont(self.fontName, 11))
    
    def initUITexts(self) -> None:
        self.title.setText("EasyClock 简易学习时钟")
        self.data.setText("Version: v0.1.0\nCode by: ymy139\n本软件遵循AGPLv3开源许可证在GitHub开源")
        self.sentenceFrom.setText("一言来源: <a href='http://hitokoto.cn'>hitokoto.cn</a>")
        self.githubRepo.setText("GitHub仓库: <a href='http://gitHub.com/ymy139/EasyClock'>gitHub.com/ymy139/EasyClock</a>")
        self.ok.setText("确认")
        
class SettingsWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.loadFonts()
        self.initWindow()
        self.initUIWidget()
        self.initUITexts()
        self.initSettingsItem()
        self.about.clicked.connect(self.showAbout)
        self.accept.clicked.connect(self.saveSettings)
        self.focusModeBackground[2].clicked.connect(self.chooseFocusModeBgImg) # type: ignore
        
    def loadFonts(self) -> None:
        fontID_ui = QFontDatabase.addApplicationFont("resources/fonts/ui.ttf")
        self.fontName = QFontDatabase.applicationFontFamilies(fontID_ui)[0]
        
    def initWindow(self) -> None:
        self.resize(520, 95)
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setWindowTitle("EasyClock - 设置")
        self.setWindowIcon(QIcon("resources/imgs/icon.ico"))
        self.setMaximumSize(520, 95)
        self.setMinimumSize(520, 95)
        
    def initUIWidget(self) -> None: 
        self.focusModeBackground: list[QWidget] = [
            QLabel(self),
            LineEdit(self),
            ToolButton(self)
        ]
        self.focusModeBackground[0].setGeometry(10, 5, 130, 25)
        self.focusModeBackground[0].setFont(QFont(self.fontName, 12))
        self.focusModeBackground[1].setGeometry(10, 35, 395, 33)
        self.focusModeBackground[2].setGeometry(410, 35, 35, 33)
        self.focusModeBackground[2].setIcon(FluentIcon.MORE) # type: ignore
        
        self.alwaysOnTop = CheckBox(self)
        self.alwaysOnTop.setGeometry(360, 5, 85, 22)
        
        self.about = PushButton(self)
        self.about.setGeometry(455, 5, 60, 30)
        
        self.accept = PushButton(self)
        self.accept.setGeometry(455, 40, 60, 30)
        
        self.statusBar = QLabel(self)
        self.statusBar.setGeometry(0, 75, 520, 20)
        self.statusBar.setStyleSheet("background-color: #F0F0F0;")
        
    def initUITexts(self) -> None:
        self.focusModeBackground[0].setText("专注模式背景图片") # type: ignore
        self.focusModeBackground[1].setPlaceholderText("输入图片路径或点击右侧按钮选择文件") # type: ignore
        self.alwaysOnTop.setText("窗口置顶")
        self.about.setText("关于")
        self.accept.setText("应用")
        
    def initSettingsItem(self) -> None:
        settings = Funcs.Settings.readSettings()
        if settings["window"]["alwaysOnTop"] == True: # type: ignore
            self.alwaysOnTop.setChecked(True)
        self.focusModeBackground[1].setText(settings["theme"]["focusMode"]["background"]) # type: ignore
        
    def showAbout(self) -> None:
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()
        
    def saveSettings(self) -> None:
        settings = Funcs.Settings.getSettingsFromWindow(self)
        if self.dialog.selectedMimeTypeFilter() == "application/octet-stream":
            warn = QMessageBox.warning(self, 
                                        "警告", 
                                        "您选择的图片文件可能不受支持，可能出现预料之外的错误。", 
                                        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel, 
                                        QMessageBox.StandardButton.Cancel)
            if warn == QMessageBox.StandardButton.Cancel:
                return None
        try:
            Funcs.Settings.saveSettings(settings)
            self.statusBar.setText(strftime("  %Y/%m/%d - %H:%M:%S  ") + "已保存设置，重新启动软件以生效。")
        except BaseException as errorMsg:
            self.statusBar.setText(strftime("  %Y/%m/%d - %H:%M:%S  ") + "保存失败：" + str(errorMsg))
            
    def chooseFocusModeBgImg(self) -> None:
        self.dialog = QFileDialog(self)
        self.dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.dialog.setMimeTypeFilters(["application/octet-stream", "image/jpeg", 
                                   "image/png", "image/bmp", "image/gif"])
        self.dialog.selectMimeTypeFilter("image/jpeg")
        if self.dialog.exec() == QFileDialog.DialogCode.Accepted:
            selectedFile = self.dialog.selectedFiles()[0]
            self.focusModeBackground[1].setText(selectedFile) # type: ignore
   
class Slots(object):
    def __init__(self, window: MainWindow) -> None:
        self.window = window
        
    def ChangeAnotherSentence(self) -> None:
        sentence = Funcs.getASentence()
        self.window.sentence.setText("「"+sentence["sentence"]+"」")
        if sentence["from"] != None and sentence["from_who"] == None:
            self.window.sentenceFrom.setText("——「"+sentence["from"]+"」")
        elif sentence["from"] == None and sentence["from_who"] != None:
            self.window.sentenceFrom.setText("——"+sentence["from_who"])
        else:
            self.window.sentenceFrom.setText("——"+sentence["from_who"]+"「"+sentence["from"]+"」")
            
    def addToDoItem(self) -> None:
        newItem = QListWidgetItem(self.window.toDoList)
        newItem.setText("新建待办事项")
        newItem.setFlags(Qt.ItemFlag.ItemIsEditable | 
                        Qt.ItemFlag.ItemIsSelectable | 
                        Qt.ItemFlag.ItemIsDragEnabled | 
                        Qt.ItemFlag.ItemIsUserCheckable | 
                        Qt.ItemFlag.ItemIsEnabled)

    def delToDoItem(self) -> None:
        currentItem = self.window.toDoList.currentItem()
        if currentItem != None:
            row = self.window.toDoList.row(currentItem)
            self.window.toDoList.takeItem(row)
        
    def updataWindow(self) -> None:
        try:
            while True:
                nowTime = Funcs.getNowTime()
                lunarDay = Funcs.solarToLunar(int(strftime("%Y")), 
                                            int(strftime("%m")), 
                                            int(strftime("%d")))
                
                self.window.timeWidget["hour"].setText(nowTime["hour"])
                self.window.timeWidget["minute"].setText(nowTime["minute"])
                self.window.timeWidget["second"].setText(nowTime["second"])
                
                self.window.date.setText(strftime("%Y年%m月%d日")+" "+
                                    nowTime["weekday"]+" "+
                                    Funcs.getLunarDateString(lunarDay[1], lunarDay[2]))
                
                self.window.countdown.setText("高考倒计时："+str(Funcs.calculateCountdown(6, 7))+"天")
                
                QApplication.processEvents()
                sleep(0.2)
        except: pass
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # win = MainWindow()
    # win = AboutWindow()
    win = SettingsWindow()
    win.show()
    exit(app.exec())