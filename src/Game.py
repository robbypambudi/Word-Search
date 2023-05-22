import random
import string
import tkinter as tk
import yaml
import src.gameUtils as gutils
import tkinter.messagebox as msg
import src.time_1 as t
import src.help as h

wordPressed = ''
previous = [0, 0]
route = [0, 0]


def startGame(root):
    config = gutils.readConfigFile()
    levelNum = config['player']['level']

    # Timer Frame
    frame = tk.Frame(root, bg="white", width=400, height=100)
    frame.pack(fill=tk.BOTH, side=tk.TOP)
    t.timer(frame, config['levels'][levelNum]['time'])

    # Vertical Frame
    frame1 = tk.Frame(master=root, bg="red")
    frame1.pack(side=tk.LEFT, expand=True, padx=20, pady=20)
    frame1.grid_columnconfigure(0, weight=1)

    levelDetails = [
        config['levels'][levelNum]['name'],
        config['levels'][levelNum]['words']
    ]
    currScore = tk.StringVar()
    currScore.set(0)

    def updateScore():
        config = gutils.readConfigFile()
        score = config['player']['score']
        config['player']['score'] = score + 1
        currScore.set(score + 1)
        gutils.writeConfigFile(config)
        root.update_idletasks()

    frame3 = tk.Frame(master=root)
    frame3.pack(fill=tk.BOTH, side=tk.RIGHT, padx=20, pady=30)

    frame4 = tk.Frame(master=root, bg='#cbe5f7', width=400)
    frame4.pack(fill=tk.BOTH, side=tk.TOP, pady=10, anchor='ne', expand=True)

    gutils.labelGame(frame3, config, levelDetails, currScore)

    wordList = []

    with open(r'data/words.yaml') as file:
        wordFile = yaml.load(file, Loader=yaml.FullLoader)
        wordData = wordFile['words']
        wordList = [word for word in wordFile['words']]

    numWords = config['words_count']
    size = config['word_count']

    arr = [[0 for x in range(size)] for y in range(size)]
    button = [[0 for x in range(size)] for y in range(size)]
    check = [0 for numWords in range(size)]
    dictionary = [0 for createWordSet in range(numWords)]

    directionArr = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1],
                    [0, -1], [1, -1]]

    def handleButtonHelp():
        h.help(root, arr, button, dictionary, wordData)

    def nextLevel():
        config = gutils.readConfigFile()
        config['player']['level'] = config['player']['level'] + 1
        gutils.writeConfigFile(config)
        frame.destroy()
        frame1.destroy()
        frame4.destroy()
        frame3.destroy()
        if (config['player']['level'] == 4):
            msg.showinfo("Selamat!", "Anda telah menyelesaikan semua level!")
            endFrame = tk.Frame(root, bg="white", width=400, height=100)
            endFrame.pack(fill=tk.BOTH, side=tk.TOP)
            tk.Label(endFrame, text="Score Anda: " +
                     str(config['player']['score']), font=("Open Sans", 12, "bold")).pack(pady=10)

            button_keluar = tk.Button(endFrame, text="Keluar", font=(
                "Open Sans", 12), fg='black', bg='red', borderwidth=0, highlightthickness=0, command=root.destroy)
            button_keluar.pack(pady=(0, 20), ipadx=20,
                               ipady=10, anchor=tk.CENTER)

            endFrame.update_idletasks()

            width = endFrame.winfo_width()
            height = endFrame.winfo_height()

            x = (endFrame.winfo_screenwidth() // 2) - (width // 2)
            y = (endFrame.winfo_screenheight() // 2) - (height // 2)

            endFrame.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        else:
            startGame(root)

    tk.Button(frame, text="Bantuan", font=("Open Sans", 12), fg='black', bg='yellow',
              borderwidth=0, highlightthickness=0, command=handleButtonHelp).pack(side=tk.RIGHT, padx=10)

    tk.Button(frame, text="Next Level", font=("Open Sans", 12), fg='black', bg='green',
              borderwidth=0, highlightthickness=0, command=nextLevel).pack(side=tk.LEFT, padx=10)

    class Square:
        status = False
        filled = False
        char = ''

    def fill(x, y, word, direction):
        w = wordData[word]['WORD']
        for i in range(len(w)):
            arr[x + direction[0] * i][y + direction[1] * i].char = w[i]
            arr[x + direction[0] * i][y + direction[1] * i].filled = True
        wordList.remove(word)

    def wordPlace(j, dictionary):
        word = random.choice(wordList)
        direction = directionArr[random.randrange(0, 7)]
        oneWord = wordData[word]['WORD']
        x = random.randrange(0, size - 1)
        y = random.randrange(0, size - 1)

        if (x + len(oneWord) * direction[0] > size - 1
                or x + len(oneWord) * direction[0] < 0
                or y + len(oneWord) * direction[1] > size - 1
            ) or y + len(oneWord) * direction[1] < 0:
            wordPlace(j, dictionary)
            return

        for i in range(len(oneWord)):
            if (arr[x + direction[0] * i][y +
                                          direction[1] * i].filled == True):
                if (arr[x + direction[0] * i][y + direction[1] * i].char !=
                        oneWord[i]):
                    wordPlace(j, dictionary)
                    return
        dictionary[j] = {
            'WORD': oneWord,
            'HINT': wordData[word]['HINT'],
            'IS_HELPED': False,
        }

        check[j] = tk.Label(frame4,
                            text=wordData[word]['HINT'],
                            height=1,
                            width=50,
                            font=('None %d ' % (10)),
                            fg='#254359',
                            bg='#cbe5f7',
                            anchor='c')
        check[j].grid(row=j+1, column=0, padx=3, pady=2)

        fill(x, y, word, direction)
        return dictionary

    def colourWord(wordPressed, valid):
        route[0] *= -1
        route[1] *= -1
        for i in range(len(wordPressed)):
            if valid == True or arr[previous[0] +
                                    i * route[0]][previous[1] +
                                                  i * route[1]].status == True:
                button[previous[0] + i * route[0]][previous[1] +
                                                   i * route[1]].config(
                                                       bg='#535edb',
                                                       fg='white')
                arr[previous[0] + i * route[0]][previous[1] +
                                                i * route[1]].status = True
            elif (arr[previous[0] +
                      i * route[0]][previous[1] +
                                    i * route[1]].status == False):
                button[previous[0] + i * route[0]][previous[1] +
                                                   i * route[1]].config(
                                                       bg='#255059',
                                                       fg='white')

    def checkWord():
        global wordPressed
        dict = [dictionary[i]['WORD']
                for i in range(len(dictionary)) if dictionary[i] != '']

        if wordPressed in dict and wordPressed != '':
            check[int(dict.index(wordPressed))].configure(
                font=('Helvetica', 10),  fg='green',
                bg='#cbe5f7',)

            updateScore()
            colourWord(wordPressed, True)
        else:
            colourWord(wordPressed, False)
        wordPressed = ''
        previous = [0, 0]

    def buttonPress(x, y):
        global wordPressed, previous, route
        newPressed = [x, y]

        if (len(wordPressed) == 0):
            previous = newPressed
            wordPressed = arr[x][y].char
            button[x][y].configure(bg='#2c334a', fg='white')

        elif (len(wordPressed) == 1 and (x - previous[0])**2 <= 1
              and (y - previous[1])**2 <= 1 and newPressed != previous):
            wordPressed += arr[x][y].char
            button[x][y].configure(bg='#2c334a', fg='white')

            route = [x - previous[0], y - previous[1]]
            previous = [x, y]

        elif (len(wordPressed) > 1 and x - previous[0] == route[0]
              and y - previous[1] == route[1]):
            wordPressed += arr[x][y].char
            button[x][y].configure(bg='#2c334a', fg='white')
            previous = [x, y]

    for x in range(size):
        for y in range(size):
            arr[x][y] = Square()

    for i in range(numWords):
        wordPlace(i, dictionary)

    for y in range(size):
        for x in range(size):

            if (arr[x][y].filled == False):
                arr[x][y].char = random.choice(string.ascii_uppercase)

            # Button in Grid
            button[x][y] = tk.Button(
                frame1,
                text=arr[x][y].char,
                bg='#255059',
                fg='white',
                width=4,
                height=2,
                relief=tk.FLAT,
                font=('Helvetica', 9),
                command=lambda x=x, y=y: buttonPress(x, y))
            button[x][y].grid(row=x, column=y)

    checkWordBtn = tk.Button(frame4,
                             text="Check Word",
                             height=1,
                             width=15,
                             anchor='c',
                             bg="#70889c",
                             font=('Helvetica', 10),
                             fg='white',
                             command=checkWord)
    checkWordBtn.grid(row=0, column=0)
