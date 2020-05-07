import winsound
import time


def sound(result):
    """Function plays sound beep in windows"""
    for character in result:
        if character == '.':
            winsound.Beep(1200, 500)
            time.sleep(0.5)
        elif character == '-':
            winsound.Beep(4000, 500)
            time.sleep(0.5)
        elif character == ' ':
            time.sleep(1)
