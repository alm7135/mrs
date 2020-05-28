import datetime
import os
import re
import time
import tkinter as tk
import uuid
from tkinter import messagebox

import keyboard
import mysql.connector
import simpleaudio as sa

offline = False
ROOT_DIR = os.path.dirname(__file__)
# Audio files for morse code playback.
dot = ROOT_DIR + "\\dit.wav"
underscore = ROOT_DIR + "\\dah.wav"
gap = ROOT_DIR + "\\gap.wav"
audiolength = 0.119

lists = []

# Query for sending data to database
query = 'INSERT INTO messages (message, morse, mac, playback_time, aired) VALUES (%s, %s, %s, %s, %s)'
# MAC for identification
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
# Connection to database


try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='mcdb'
    )
    cursor = db.cursor()
except:
    print("Connection error, program will continue in offline mode.")
    offline = True

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
                decipher += list(MORSE_CODE_DICT.keys()
                                 )[list(MORSE_CODE_DICT.values()).index(cite)]
                cite = ''
    return decipher


def sound(result):
    """Function plays sound beep in windows"""
    for character in result:
        if character == '.':
            lists.append(dot)
            wave_obj = sa.WaveObject.from_wave_file(dot)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        elif character == '-':
            lists.append(underscore)
            wave_obj = sa.WaveObject.from_wave_file(underscore)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        elif character == ' ':
            lists.append(gap)
            time.sleep(.1)


root = tk.Tk()
canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()
label1 = tk.Label(root, text='Text to morse')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)
label2 = tk.Label(root, text='Type your text:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)
entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def button():
    message = entry1.get()
    if message != "":
        tenor = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = encrypt(message.upper())
        messageLength = int(audiolength * len(result) + 1)
        label3 = tk.Label(root, text='Encrypted text:', font=('helvetica', 10))
        canvas1.create_window(200, 210, window=label3)
        label4 = tk.Label(root, text=result, font=('helvetica', 10, 'bold'))
        canvas1.create_window(200, 230, window=label4)
        print("Sound duration " + messageLength.__str__() + " s")
        sound(result)
        if not offline:
            val = (message, result, mac, messageLength, tenor)
            cursor.execute(query, val)
            db.commit()


def button2():
    if not offline:
        tempfile = open(ROOT_DIR + "\\temp.txt", "w")
        cursor.execute("select message, mac, aired from messages")
        res = cursor.fetchall()
        for row in res:
            tempfile.write(row[1] + " at " +
                           row[2].strftime("%Y-%m-%d %H:%M:%S"))
            tempfile.write("\n" + row[0] + "\n\n")
        tempfile.close()
    else:
        messagebox.showerror("connection error",
                             "cant refresh while in offline mode")


button1 = tk.Button(text='Enter', command=button, bg='brown', fg='white',
                    font=('helvetica', 9, 'bold'))

button2 = tk.Button(text='Refresh', command=button2, bg='brown', fg='white',
                    font=('helvetica', 9, 'bold'))

canvas1.create_window(200, 180, window=button1)
canvas1.create_window(350, 25, window=button2)


key_down_time = 0
key_down_length = 0
key_up_time = 0
buffer2 = ""
pressed = False

print("Ready")

start = input()
if start == "y":
    while True:
        if keyboard.is_pressed('.'):
            if not pressed:
                print(f'pressed:')
                key_down_time = time.time()
                pressed = True
        else:
            if pressed == True:
                key_up_time = time.time()
                key_down_length = key_up_time - key_down_time
                print(key_down_length)
                if 1 > key_down_length > 0.15:
                    buffer2 += "-"
                elif key_down_length >= 1:
                    buffer2 += " "
                else:
                    buffer2 += "."
                pressed = False
        if keyboard.is_pressed('c'):
            break


def main():
    """Main Function"""
    if os.path.exists("temp.txt"):
        os.remove("temp.txt")
    # root.mainloop()
    # Audio analysis
    # freq, time, interval = aa.analyzeAudio()
    # print(Code.decryptSound(freq))
    # print(freq)


# Main call
if __name__ == "__main__":
    main()
