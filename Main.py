import Decrypt as Code
import ToneSound as Sound
import AudioAnalysis as aa


def main():
    """Main Function"""
    message = input('enter text: ')
    result = Code.encrypt(message.upper())
    freq, time, interval = aa.analyzeAudio()
    print(Code.decryptSound(freq))
    print(freq)
    # Play sound in windows
    play = input('do u want to play morse code as sound? (y/n)')
    if play.upper() == 'Y':
        Sound.sound(result)


# Main call
if __name__ == "__main__":
    main()
