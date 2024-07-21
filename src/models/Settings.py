from json import loads as loadJSON
from json import dumps as dumpJSON
from os import access, F_OK, mkdir
from io import TextIOWrapper

from .Windows import SettingsWindow
from .Types import configDictType

defaultSettings: configDictType = {
    "configFmtVersion": 1,
    "window": {
        "alwaysOnTop": False,
        "countDown": {
            "month": 6,
            "day": 7,
            "text": "高考倒计时"
        }
    },
    "theme": {
        "focusMode": {
            "background": ""
        }
    }
}

def readSettings() -> configDictType:
    """read settings from `config/config.json`, if the file doesn't exist, then 
    return default settings

    Returns:
        configDictType: settings
    """
    settingsIO = _openSettings()
    settings = settingsIO.read()
    settingsIO.close()
    return loadJSON(settings)

def saveSettings(settings: configDictType) -> None:
    """save settings to `config/config.json`

    Args:
        settings (configDictType): settings to be saved

    Raises:
        FileNotFoundError: raise if the focus mode background image doesn't exist
    """
    # Determine if it is a legal configuration
    if not _isLegalConfiguration(settings) == True:
        _throwIllegalReasons(settings)
    configFileIO = _openSettings()
    configFileIO.write(dumpJSON(settings))
    configFileIO.close()
    return None

def getSettingsFromWindow(settingsWindow: SettingsWindow) -> configDictType:
    """get setting from settings window

    Args:
        settingsWindow (SettingsWindow): instantiated `SettingsWindow`

    Returns:
        configDictType: settings obtained
    """
    return {
        "configFmtVersion": 1,
        "window": {
            "alwaysOnTop": settingsWindow.alwaysOnTop.isChecked(),
            "countDown": {
                "month": settingsWindow.countDown_month_num.value(),
                "day": settingsWindow.countDown_day_num.value(),
                "text": settingsWindow.countDown_text_input.text()
            }
        },
        "theme": {
            "focusMode": {
                "background": settingsWindow.focusModeBackground_input.text()
            }
        }
    }
    
def _isLegalConfiguration(settings: configDictType) -> bool:
    """determine if it is a legal configuration

    Args:
        settings (configDictType): settings

    Returns:
        bool: is a legal configuration
    """
    if not _isFocusModeBackgroundExists(settings):
        return False
    return True

def _throwIllegalReasons(settings: configDictType) -> None:
    """throwing illegal reasons for configuration as an error

    Args:
        settings (configDictType): settings

    Raises:
        FileNotFoundError: focus mode background image file doesn't exists
    """
    if(_isFocusModeBackgroundExists(settings)):
        raise FileNotFoundError("专注模式背景图片不存在")
    
def _isFocusModeBackgroundExists(settings: configDictType) -> bool:
    """is focus mode background image file exists

    Args:
        settings (configDictType): settings

    Returns:
        bool: is exists
    """
    if (# not empty...
        not settings["theme"]["focusMode"]["background"] == "" and # type: ignore
        # and file exists
        not access(settings["theme"]["focusMode"]["background"], F_OK)): # type: ignore
        return False
    return True

def _openSettings() -> TextIOWrapper:
    """open settings file.
    
    If the settings file does not exist, automatically create the file and write 
    it to the default settings

    Returns:
        TextIOWrapper: settings file IO
    """
    if not access("config", F_OK):
        mkdir("config")
    
    if not access("config/config.json", F_OK):
        result = open("config/config.json", "a+", encoding="utf-8")
        result.write(dumpJSON(defaultSettings))
    else:
        result = open("config/config.json", "r+", encoding="utf-8")
        
    return result

# idk why, but i need to do this, otherwise, the loadJSON function will throw an error during the first run
# maybe it's because I'm not skilled enough
_openSettings().close()