import Decrypt as morse


def main():
    message = input('enter text: ')
    result = morse.encrypt(message.upper())
    print(result)


if __name__ == "__main__":
    main()
