import Decrypt as morse
import winsound
import time


def main():
    message = input('enter text: ')
    result = morse.encrypt(message.upper())
    print(result)
    for charachter in result:
        if charachter == '.':
            winsound.Beep(400, 500)
            time.sleep(0.5)
        elif charachter == '-':
            winsound.Beep(1000, 500)
            time.sleep(0.5)
        elif charachter == ' ':
            time.sleep(1)
    Sveiki cia naujas bandymas

if __name__ == "__main__":
    main()
