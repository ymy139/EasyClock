from datetime import date as Date
from time import strftime
from lunardate import LunarDate

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