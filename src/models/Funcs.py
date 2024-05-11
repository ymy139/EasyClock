from datetime import date as Date
from time import strftime
from json import loads as loadJSON
from json import dumps as dumpJSON
from random import randint
from lunardate import LunarDate
from os import access, F_OK, mkdir

from .Windows import SettingsWindow
from .Types import configDictType

def getGreetingSentence(hour: int) -> str:
    """get a greeting sentence

    Args:
        hour (int): a 24-hour clock number

    Returns:
        str: a greeting sentence
    """
    greetingSentences = {
        0: "新的一天开始了，愿你充满活力，迎接每一个挑战，享受每一份喜悦！",
        1: "新的一天开始了，愿你充满活力，迎接每一个挑战，享受每一份喜悦！",
        2: "新的一天开始了，愿你充满活力，迎接每一个挑战，享受每一份喜悦！",
        3: "新的一天开始了，愿你充满活力，迎接每一个挑战，享受每一份喜悦！",
        4: "新的一天开始了，愿你充满活力，迎接每一个挑战，享受每一份喜悦！",
        5: "新的一天开始了，愿你充满活力，迎接每一个挑战，享受每一份喜悦！",
        6: "新的一天开始了，愿你充满活力，迎接每一个挑战，享受每一份喜悦！",
        7: "早上好，愿你充满活力和希望，享受每一个美好的瞬间！",
        8: "早上好，愿你充满活力和希望，享受每一个美好的瞬间！",
        9: "早上好，愿你充满活力和希望，享受每一个美好的瞬间！",
        10:"早上好，愿你充满活力和希望，享受每一个美好的瞬间！",
        11:"早上好，愿你充满活力和希望，享受每一个美好的瞬间！",
        12:"中午好，希望你的一天过得充实而愉快，保持好心情，继续前行！",
        13:"中午好，希望你的一天过得充实而愉快，保持好心情，继续前行！",
        14:"下午好，愿你在这个美好的时光里，收获满满的喜悦与幸福。",
        15:"下午好，愿你在这个美好的时光里，收获满满的喜悦与幸福。",
        16:"下午好，愿你在这个美好的时光里，收获满满的喜悦与幸福。",
        17:"下午好，愿你在这个美好的时光里，收获满满的喜悦与幸福。",
        18:"晚上好，愿你的夜晚如同星空般璀璨，充满宁静与美好。",
        19:"晚上好，愿你的夜晚如同星空般璀璨，充满宁静与美好。",
        20:"晚上好，愿你的夜晚如同星空般璀璨，充满宁静与美好。",
        21:"夜色温柔，月光如水，此刻的宁静是为你准备的，早些休息吧，晚安！",
        22:"夜色温柔，月光如水，此刻的宁静是为你准备的，早些休息吧，晚安！ ",
        23:"夜色温柔，月光如水，此刻的宁静是为你准备的，早些休息吧，晚安！"
    }
    return greetingSentences[hour]

def calculateCountdown(targetMonth: int, targetDay: int) -> int:
    """calculate the countdown days to the target date

    Args:
        targetMonth (int): target month
        targetDay (int): target day

    Returns:
        int: the countdown, if the target is today, return 0
    """
    today = Date.today()
    targetYear = today.year
    nextTargetDate = Date(targetYear, targetMonth, targetDay)
    if nextTargetDate < today:
        targetYear += 1
        nextTargetDate = Date(targetYear, targetMonth, targetDay)
    delta = nextTargetDate - today
    return delta.days if delta.days > 0 else 0

def getASentence() -> dict[str, str]:
    """get a sentence

    Returns:
        dict[str, str]: a dict, like this:
            ```json
            {
                "sentence": "...",
                "from": "...",
                "from_who": "..."
            }
            ```
    """
    data: list[dict] = loadJSON(
        open("resources/data/sentences.json", encoding="utf-8")
        .read()
    )
    count = randint(0, len(data)-1)
    
    if data[count]["from_who"] == None:
        length_from = len(data[count]["from"])
    elif data[count]["from"] == None:
        length_from = len(data[count]["from_who"])
    else:
        length_from = len(data[count]["from"]) + len(data[count]["from_who"])
    
    while data[count]["length"] >= 37 or length_from >= 16:
        count = randint(0, len(data)-1)
        if data[count]["from_who"] == None:
            length_from = len(data[count]["from"])
        elif data[count]["from"] == None:
            length_from = len(data[count]["from_who"])
        else:
            length_from = len(data[count]["from"]) + len(data[count]["from_who"])
        
    return {
        "sentence": data[count]["hitokoto"],
        "from": data[count]["from"],
        "from_who": data[count]["from_who"]
    }
    
def solarToLunar(year: int, month: int, day: int) -> list[int]:
    """get lunar date from solar date

    Args:
        year (int): solar year
        month (int): solar month
        day (int): solar day

    Returns:
        list[int]: lunar date, like this: [2024, 1, 1]
    """
    lunarDate = LunarDate.fromSolarDate(year, month, day)
    lunarYear = lunarDate.year
    lunarMonth = lunarDate.month
    lunarDay = lunarDate.day
    return [lunarYear, lunarMonth, lunarDay]

def getLunarDateString(lunarMonth: int, lunarDay: int) -> str:
    """get Chinese date from lunar date

    Args:
        lunarMonth (int): lunar month
        lunarDay (int): lunar day

    Returns:
        str: Chinese date string, like this:'腊月初五'
    """ 
    chineseNums = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", 
                   "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                   "甘一", "甘二", "甘三", "甘四", "甘五", "甘六", "甘七", "甘八", "甘九", "三十",
                   "三一"]
    lunardateString = ""
    
    if lunarMonth == 1:
        lunardateString += "正月"
    elif lunarMonth == 12:
        lunardateString += "腊月"
    else:
        lunardateString += (chineseNums[lunarMonth]+"月")
        
    if lunarDay <= 10:
        lunardateString += ("初"+chineseNums[lunarDay])
    else:
        lunardateString += chineseNums[lunarDay]
        
    return lunardateString

def getNowTime() -> dict[str, str]:
    """return now time, use 24-hour clock

    Returns:
        dict[str, int]: now time, like this:
        ```json
        {
            "hour": "23",
            "minute": "59",
            "second": "59",
            "weekday": "星期日"
        }
        ```
    """
    weekdays = {
        "Monday": "星期一",
        "Tuesday": "星期二",
        "Wednesday": "星期三",
        "Thursday": "星期四",
        "Friday": "星期五",
        "Saturday": "星期六",
        "Sunday": "星期日"
    }
    return {
        "hour": strftime("%H"),
        "minute": strftime("%M"),
        "second": strftime("%S"),
        "weekday": weekdays[strftime("%A")]
    }
    
class Settings():
    defaultSettings: configDictType = {
        "configFmtVersion": 1,
        "window": {
            "alwaysOnTop": False
        },
        "theme": {
            "focusMode": {
                "background": ""
            }
        }
    }
    
    @staticmethod
    def readSettings() -> configDictType:
        if access("config/config.json", F_OK):
            return loadJSON(open("config/config.json", "r", encoding="utf-8")
                            .read())
        else:
            return Settings.defaultSettings
    
    @staticmethod
    def saveSettings(settings: configDictType) -> None:
        # Determine if it is a legal configuration
        if not access(settings["theme"]["focusMode"]["background"], F_OK): # type: ignore
            raise FileNotFoundError("专注模式背景图片不存在！")
        
        if not access("config", F_OK):
            mkdir("config")
        configFile = open("config/config.json", "w", encoding="utf-8")
        configFile.write(dumpJSON(settings))
        configFile.close()
        return None
    
    @staticmethod
    def getSettingsFromWindow(settingsWindow: SettingsWindow) -> configDictType:
        return {
            "configFmtVersion": 1,
            "window": {
                "alwaysOnTop": settingsWindow.alwaysOnTop.isChecked()
            },
            "theme": {
                "focusMode": {
                    "background": settingsWindow.focusModeBackground[1].text() # type: ignore
                }
            }
        }