import win32api

def modify_resolution():
    dm = win32api.EnumDisplaySettings(None, 0)
    dm.PelsHeight = 768
    dm.PelsWidth = 1366
    dm.BitsPerPel = 32
    dm.DisplayFixedOutput = 0
    win32api.ChangeDisplaySettings(dm, 0)

if __name__ == '_main_':
    modify_resolution()