from time import strftime, sleep

from PyQt6.QtGui import QCloseEvent, QFont, QFontDatabase, QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QListWidgetItem, QFileDialog, QMessageBox
from qfluentwidgets import PushButton, ListWidget, LineEdit, CheckBox, FluentIcon, ToolButton, SpinBox

from . import Funcs, Settings, DateAndTime, Types

def _loadFonts() -> dict[str, str]:
    """load the required font

    Returns:
        dict[str, str]: a dict of font name, like this:
    ```json
    {
      "ui": "fontName",
      "time": "fontName"
    }
    ```
    """
    fontID_ui = QFontDatabase.addApplicationFont("resources/fonts/ui.ttf")
    fontID_time = QFontDatabase.addApplicationFont("resources/fonts/time.ttf")
    return {
        "ui": QFontDatabase.applicationFontFamilies(fontID_ui)[0],
        "time": QFontDatabase.applicationFontFamilies(fontID_time)[0]
    }
class MainWindow(QWidget):
    """main window"""
    def __init__(self, flags: Qt.WindowType | None = None) -> None:
        if flags != None:
            super().__init__(flags=flags)
        else:
            super().__init__()
        self._fontsName = _loadFonts()
        self._initWindow()
        self._initUIWidget()
        self._initUITexts()
        self._initUIStyleSheets()
        self.settings.clicked.connect(self._showSettings)
        self.isClose = False
        
    def _initWindow(self) -> None:
        """init window widget"""
        self.resize(640, 290)
        self.setFont(QFont(self._fontsName["ui"], 12))
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setWindowTitle("EasyClock")
        self.setWindowIcon(QIcon("resources/imgs/icon.ico"))
        self.setMaximumSize(640, 290)
        self.setMinimumSize(640, 290)
        
    def _initUIWidget(self) -> None:
        """init UI widgets"""
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
        self.timeWidget["hour"].setFont(QFont(self._fontsName["time"], 100))
        self.timeWidget["hour"].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        self.timeWidget["minute"].setGeometry(150, 0, 145, 130)
        self.timeWidget["minute"].setFont(QFont(self._fontsName["time"], 100))
        self.timeWidget["minute"].setStyleSheet("color: rgb(245, 139, 46);")
        self.timeWidget["minute"].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        self.timeWidget["second"].setGeometry(295, 85, 40, 30)
        self.timeWidget["second"].setFont(QFont(self._fontsName["time"], 27))
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
        
    def _initUITexts(self) -> None:
        """add texts for UI widget"""
        self.toDoListTitle.setText("待办列表")
        self.toDoList_del.setText("-")
        self.toDoList_add.setText("+")
        self.anotherSentence.setText("←换一句")
        self.settings.setText("设置")
        
    def _initUIStyleSheets(self) -> None:
        """apply style sheets for UI widgets"""
        self.separators["time--greeting"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["greeting--oneSentence"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["left--right"].setStyleSheet("background-color: rgb(160, 160, 160);")
        self.separators["toDoList--menuBar"].setStyleSheet("background-color: rgb(160, 160, 160);")
        
    def _showSettings(self) -> None:
        """show settings window(`SettingsWindow`)"""
        self.settingsWindow = SettingsWindow(self.windowFlags())
        self.settingsWindow.show()
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """close event"""
        self.isClose = True
        self.close()
        sleep(0.5)
        return super().closeEvent(a0)
        
class AboutWindow(QWidget):
    """about window"""
    def __init__(self, flags: Qt.WindowType) -> None:
        super().__init__(flags=flags)
        self._fontsName = _loadFonts()
        self._initWindow()
        self._initUIWidget()
        self._initUITexts()
        self.ok.clicked.connect(self.close)
        
    def _initWindow(self) -> None:
        """init window widget"""
        self.resize(385, 130)
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setWindowTitle("EasyClock - 关于")
        self.setWindowIcon(QIcon("resources/imgs/icon.ico"))
        
    def _initUIWidget(self) -> None: 
        """init UI widgets"""
        self.icon = QLabel(self)
        self.icon.setGeometry(0, 0, 100, 100)
        self.icon.setScaledContents(True)
        self.icon.setPixmap(QPixmap("resources/imgs/icon.ico"))
        
        self.title = QLabel(self)
        self.title.setGeometry(110, 0, 270, 40)
        self.title.setFont(QFont(self._fontsName["ui"], 19))
        
        self.data = QLabel(self)
        self.data.setGeometry(110, 35, 270, 60)
        self.data.setFont(QFont(self._fontsName["ui"], 10))
        
        self.sentenceFrom = QLabel(self)
        self.sentenceFrom.setGeometry(10, 95, 125, 15)
        self.sentenceFrom.setFont(QFont(self._fontsName["ui"], 9))
        self.sentenceFrom.setOpenExternalLinks(True)
        
        self.githubRepo = QLabel(self)
        self.githubRepo.setGeometry(10, 110, 250, 15)
        self.githubRepo.setFont(QFont(self._fontsName["ui"], 9))
        self.githubRepo.setOpenExternalLinks(True)
        
        self.ok = PushButton(self)
        self.ok.setGeometry(260, 95, 120, 30)
        self.ok.setFont(QFont(self._fontsName["ui"], 11))
    
    def _initUITexts(self) -> None:
        """add texts for UI widget"""
        self.title.setText("EasyClock 简易学习时钟")
        self.data.setText("Version: v0.1.0\nCode by: ymy139\n本软件遵循AGPLv3开源许可证在GitHub开源")
        self.sentenceFrom.setText("一言来源: <a href='http://hitokoto.cn'>hitokoto.cn</a>")
        self.githubRepo.setText("GitHub仓库: <a href='http://gitHub.com/ymy139/EasyClock'>gitHub.com/ymy139/EasyClock</a>")
        self.ok.setText("确认")
        
class SettingsWindow(QWidget):
    """settings window"""
    def __init__(self, flags: Qt.WindowType) -> None:
        super().__init__(flags=flags)
        self._fontsName = _loadFonts()
        self._initWindow()
        self._initUIWidget()
        self._initUITexts()
        self._initSettingsItemContent()
        self.about.clicked.connect(self._showAbout)
        self.accept.clicked.connect(self._saveSettings)
        self.focusModeBackground_choose.clicked.connect(self._chooseFocusModeBgImg)
        
    def _initWindow(self) -> None:
        """init window widget"""
        self.resize(470, 180)
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setWindowTitle("EasyClock - 设置")
        self.setWindowIcon(QIcon("resources/imgs/icon.ico"))
        self.setMaximumSize(470, 180)
        self.setMinimumSize(470, 180)
        
    def _initUIWidget(self) -> None: 
        """init UI widgets"""
        # focusModeBackground
        self.focusModeBackground_label = QLabel(self)
        self.focusModeBackground_label.setGeometry(15, 0, 130, 25)
        self.focusModeBackground_label.setFont(QFont(self._fontsName["ui"], 12))
        
        self.focusModeBackground_input = LineEdit(self)
        self.focusModeBackground_input.setGeometry(10, 25, 410, 33)
        
        self.focusModeBackground_choose = ToolButton(self)
        self.focusModeBackground_choose.setGeometry(425, 25, 35, 33)
        self.focusModeBackground_choose.setIcon(FluentIcon.MORE)
        
        # countDown
        self.countDown_label = QLabel(self)
        self.countDown_label.setGeometry(15, 60, 100, 25)
        self.countDown_label.setText("自定义倒计时")
        self.countDown_label.setFont(QFont(self._fontsName["ui"], 12))
        
        self.countDown_month_label = QLabel(self)
        self.countDown_month_label.setGeometry(20, 85, 20, 33)
        self.countDown_month_label.setFont(QFont(self._fontsName["ui"], 12))
        self.countDown_month_label.setText("月")
        
        self.countDown_month_num = SpinBox(self)
        self.countDown_month_num.setGeometry(45, 85, 110, 33)
        self.countDown_month_num.setMinimum(1)
        self.countDown_month_num.setMaximum(12)
        
        self.countDown_day_label = QLabel(self)
        self.countDown_day_label.setGeometry(160, 85, 20, 33)
        self.countDown_day_label.setFont(QFont(self._fontsName["ui"], 12))
        self.countDown_day_label.setText("日")
        
        self.countDown_day_num = SpinBox(self)
        self.countDown_day_num.setGeometry(185, 85, 110, 33)
        self.countDown_day_num.setMinimum(1)
        self.countDown_day_num.setMaximum(31)
        
        self.countDown_text_label = QLabel(self)
        self.countDown_text_label.setGeometry(20, 125, 80, 25)
        self.countDown_text_label.setFont(QFont(self._fontsName["ui"], 12))
        self.countDown_text_label.setText("倒计时内容")
        
        self.countDown_text_input = LineEdit(self)
        self.countDown_text_input.setGeometry(105, 120, 190, 33)
        
        self.alwaysOnTop = CheckBox(self)
        self.alwaysOnTop.setGeometry(355, 80, 85, 22)
        
        self.about = PushButton(self)
        self.about.setGeometry(340, 120, 60, 33)
        
        self.accept = PushButton(self)
        self.accept.setGeometry(405, 120, 60, 33)
        
        self.statusBar = QLabel(self)
        self.statusBar.setGeometry(0, 160, 470, 20)
        self.statusBar.setStyleSheet("background-color: #F0F0F0;")
        
    def _initUITexts(self) -> None:
        """add texts for UI widget"""
        self.focusModeBackground_label.setText("专注模式背景图片")
        self.focusModeBackground_input.setPlaceholderText("输入图片路径或点击右侧按钮选择文件")
        self.countDown_text_input.setPlaceholderText("这将显示在倒计时之前")
        self.alwaysOnTop.setText("窗口置顶")
        self.about.setText("关于")
        self.accept.setText("应用")
        
    def _initSettingsItemContent(self) -> None:
        """write settings item content to widgets"""
        settings = Settings.readSettings()
        if settings["window"]["alwaysOnTop"] == True: # type: ignore
            self.alwaysOnTop.setChecked(True)
        self.focusModeBackground_input.setText(settings["theme"]["focusMode"]["background"]) # type: ignore
        self.countDown_month_num.setValue(settings["window"]["countDown"]["month"]) # type: ignore
        self.countDown_day_num.setValue(settings["window"]["countDown"]["day"]) # type: ignore
        self.countDown_text_input.setText(settings["window"]["countDown"]["text"]) # type: ignore
        
    def _showAbout(self) -> None:
        """show about window(`AboutWindow`)"""
        self.aboutWindow = AboutWindow(self.windowFlags())
        self.aboutWindow.show()
        
    def _saveSettings(self) -> None:
        """save settings (I don't think this function should be placed here)"""
        settings = Settings.getSettingsFromWindow(self)
        if getattr(self, "dialog", None) != None and self.dialog.selectedMimeTypeFilter() == "application/octet-stream":
            warn = QMessageBox.warning(self, 
                                        "警告", 
                                        "您选择的图片文件可能不受支持，可能出现预料之外的错误。", 
                                        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel, 
                                        QMessageBox.StandardButton.Cancel)
            if warn == QMessageBox.StandardButton.Cancel:
                return None
        try:
            Settings.saveSettings(settings)
            self.statusBar.setText(strftime("  %Y/%m/%d - %H:%M:%S  ") + "已保存设置，重新启动软件以生效。")
        except BaseException as errorMsg:
            self.statusBar.setText(strftime("  %Y/%m/%d - %H:%M:%S  ") + "保存失败：" + str(errorMsg))
            
    def _chooseFocusModeBgImg(self) -> None:
        """open the file selection window to select focus mode background image file, and auto write 
           the file path to the widget"""
        self.dialog = QFileDialog(self)
        self.dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.dialog.setMimeTypeFilters(["application/octet-stream", "image/jpeg", 
                                   "image/png", "image/bmp", "image/gif"])
        self.dialog.selectMimeTypeFilter("image/jpeg")
        if self.dialog.exec() == QFileDialog.DialogCode.Accepted:
            selectedFile = self.dialog.selectedFiles()[0]
            self.focusModeBackground_input.setText(selectedFile)
   
class Slots(object):
    """slots for the windows"""
    def __init__(self, window: MainWindow) -> None:
        self.window = window
        
    def ChangeAnotherSentence(self) -> None:
        """change another sentence for main window(`MainWindow`)"""
        sentence = Funcs.getASentence()
        self.window.sentence.setText("「"+sentence["sentence"]+"」")
        if sentence["from"] != None and sentence["from_who"] == None:
            self.window.sentenceFrom.setText("——「"+sentence["from"]+"」")
        elif sentence["from"] == None and sentence["from_who"] != None:
            self.window.sentenceFrom.setText("——"+sentence["from_who"])
        else:
            self.window.sentenceFrom.setText("——"+sentence["from_who"]+"「"+sentence["from"]+"」")
            
    def addToDoItem(self) -> None:
        """add To Do Item"""
        newItem = QListWidgetItem(self.window.toDoList)
        newItem.setText("新建待办事项")
        newItem.setFlags(Qt.ItemFlag.ItemIsEditable |
                         Qt.ItemFlag.ItemIsSelectable |
                         Qt.ItemFlag.ItemIsDragEnabled |
                         Qt.ItemFlag.ItemIsUserCheckable |
                         Qt.ItemFlag.ItemIsEnabled)

    def delToDoItem(self) -> None:
        """delate To Do Items"""
        currentItem = self.window.toDoList.currentItem()
        if currentItem != None:
            row = self.window.toDoList.row(currentItem)
            self.window.toDoList.takeItem(row)
        
    def updataWindowLoop(self) -> None:
        """window update loop, should run within a separate thread"""
        while not self.window.isClose:
            nowTime = DateAndTime.getNowTime()
            settings = Settings.readSettings()
            lunarDay = DateAndTime.solarToLunar(int(strftime("%Y")), int(strftime("%m")), int(strftime("%d")))
            self._updataTime(nowTime)
            self._updataData(nowTime, lunarDay)
            self._updataGreeting(int(strftime("%H")))
            self._updataCountDown(settings)
            self._updataApplication()
            sleep(0.2)
                
    def _updataTime(self, nowTime: dict[str, str]) -> None:
        """updata the time info for main window(`MainWindow`)"""
        self.window.timeWidget["hour"].setText(nowTime["hour"])
        self.window.timeWidget["minute"].setText(nowTime["minute"])
        self.window.timeWidget["second"].setText(nowTime["second"])
            
    def _updataData(self, nowTime: dict[str, str], lunarDay: list[int]) -> None:
        """updata the data info for main window(`MainWindow`)(include lunar data)"""
        data = strftime("%Y年%m月%d日")
        weekday = nowTime["weekday"]
        lunarDate = DateAndTime.getLunarDateString(lunarDay[1], lunarDay[2])
        self.window.date.setText(data + " " + weekday + " " + lunarDate)
        
    def _updataGreeting(self, hour: int) -> None:
        """updata the greeting sentence for main window(`MainWindow`)"""
        greetingSentence = Funcs.getGreetingSentence(hour)
        self.window.greeting.setText(greetingSentence)
        
    def _updataCountDown(self, settings: Types.configDictType) -> None:
        """updata the count down info for main window(`MainWindow`)"""
        countDownText = settings["window"]["countDown"]["text"] # type: ignore
        countdownTargetDay: int = settings["window"]["countDown"]["day"] # type: ignore
        countdownTargetMonth: int = settings["window"]["countDown"]["month"] # type: ignore
        countdown = DateAndTime.calculateCountdown(countdownTargetMonth, countdownTargetDay)
        self.window.countdown.setText(countDownText + ": " + str(countdown) + "天") # type: ignore
        
    @staticmethod
    def _updataApplication() -> None:
        """just repackaged `QApplication.processEvents()` function"""
        QApplication.processEvents()