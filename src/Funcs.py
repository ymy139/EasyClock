from datetime import date as Date
from json import loads as loadJSON
from random import randint

def getGreetingSentence(hour: int) -> str:
    """get a greeting sentence

    Args:
        hour (int): a 24 hour number

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
        dict[str, str]: a dict, like this:{"sentence":"...","from":"...","from_who":"..."}
    """
    data: list[dict] = loadJSON(
        open("resources/data/sentences.json", encoding="utf-8")
        .read()
    )
    count = randint(0, len(data)-1)
    return {
        "sentence": data[count]["hitokoto"],
        "from": data[count]["from"],
        "from_who": data[count]["from_who"]
    }
    