import AudioAnalysis as aa
import tkinter, mysql.connector, re, uuid, time, wave, contextlib, datetime, os
import simpleaudio as sa

ROOT_DIR = os.path.dirname(__file__)
# Audio files for morse code playback.
dot = ROOT_DIR + "\\dit.wav"
underscore = ROOT_DIR + "\\dah.wav"
gap = ROOT_DIR + "\\gap.wav"
audiolength = 0.119

# Query for sending data to database
query = 'INSERT INTO messages (message, morse, mac, playback_time, aired) VALUES (%s, %s, %s, %s, %s)'

# MAC for identification
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
list = []

# Connection to database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='mcdb'
)
cursor = db.cursor()

# Morse dictionary
MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def encrypt(message):
    """Returns text input encrypted to morse code."""
    cipher = ''
    for letter in message:
        if letter != ' ':
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            cipher += ' '

    return cipher


def decrypt(message):
    """Returns decryption of morse code."""
    message += ' '
    decipher = ''
    cite = ''
    for letter in message:
        if letter != ' ':
            i = 0
            cite += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(cite)]
                cite = ''
    return decipher


def sound(result):
    """Function plays sound beep in windows"""
    for character in result:
        if character == '.':
            list.append(dot)
            wave_obj = sa.WaveObject.from_wave_file(dot)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        elif character == '-':
            list.append(underscore)
            wave_obj = sa.WaveObject.from_wave_file(underscore)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        elif character == ' ':
            list.append(gap)
            time.sleep(.1)

def main():
    """Main Function"""
    message = input('enter text: ')
    timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = encrypt(message.upper())
    messageLength = int(audiolength * len(result))
    val = (message, result, mac, messageLength, timenow)
    cursor.execute(query, val)
    db.commit()
    print('Message was succesfully sent to the database.')

    print("Sound duration " + messageLength.__str__() + " s")
    print(result)
    sound(result)

    # Audio analysis
    # freq, time, interval = aa.analyzeAudio()
    # print(Code.decryptSound(freq))
    # print(freq)


# Main call
if __name__ == "__main__":
    main()