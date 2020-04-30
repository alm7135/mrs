import Decrypt as Code
import ToneSound as Sound


def main():
    """Main Function"""
    message = input('enter text: ')
    result = Code.encrypt(message.upper())
    print(result)
    # Play sound in windows
    play = input('do u want to play morse code as sound? (y/n)')
    if play.upper() == 'Y':
        Sound.sound(result)


# Main call
if __name__ == "__main__":
    main()
