import random
import string
import tkinter as tk
import yaml
import gameUtils as gutils

wordPressed = ''
previous = [0, 0]
route = [0, 0]

def startGame(root):
    # Vertical Frame
    frame1 = tk.Frame(master=root, bg="red")
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=20, pady=20)

    frame2 = tk.Frame(master=root)
    frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=12)

    config = gutils.readConfigFile()
    levelNum = config['player']['level']
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

    abelWelcome = tk.Label(master=frame3,
                            text="Welcome",
                            fg='#2c334a',
                            font=('Helvetica', 12, 'bold')).grid(row=0,
                                                                 column=0)

    labelWName = tk.Label(master=frame3,
                          text=config['player']['name'],
                          fg='#2c334a',
                          font=('Helvetica', 12, 'bold')).grid(row=0, column=1)

    labelLevelLbl = tk.Label(master=frame3,
                             text="Level",
                             fg='#2c334a',
                             font=('Helvetica', 12)).grid(row=1, column=0)

    labelLevel = tk.Label(master=frame3,
                          text=levelDetails[0],
                          fg='#2c334a',
                          font=('Helvetica', 12, 'bold')).grid(row=1, column=1)

    labelLevelLbl = tk.Label(master=frame3,
                             text="Words",
                             fg='#2c334a',
                             font=('Helvetica', 12)).grid(row=2, column=0)

    labelLevel = tk.Label(master=frame3,
                          text=levelDetails[1],
                          fg='#2c334a',
                          font=('Helvetica', 12, 'bold')).grid(row=2, column=1)

    labelLevelLbl = tk.Label(master=frame3,
                             text="Score",
                             fg='#2c334a',
                             font=('Helvetica', 12)).grid(row=3, column=0)

    labelLevel = tk.Label(master=frame3,
                          textvariable=currScore,
                          fg='#2c334a',
                          font=('Helvetica', 12, 'bold')).grid(row=3, column=1)
    
    wordList = []

    with open(r'data/words.yaml') as file:
        wordFile = yaml.load(file, Loader=yaml.FullLoader)
        wordList = [word for word in wordFile['words']]

    size = numWords = config['words_count']

    arr = [[0 for x in range(size)] for y in range(size)]
    button = [[0 for x in range(size)] for y in range(size)]
    check = [0 for numWords in range(size)]
    dictionary = [0 for createWordSet in range(numWords)]

    directionArr = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1],
                    [0, -1], [1, -1]]

    class Square:
        status = False
        filled = False
        char = ''

    def fill(x, y, word, direction):
        for i in range(len(word)):
            arr[x + direction[0] * i][y + direction[1] * i].char = word[i]
            arr[x + direction[0] * i][y + direction[1] * i].filled = True

    def wordPlace(j, dictionary):
        word = random.choice(wordList)
        direction = directionArr[random.randrange(0, 7)]

        x = random.randrange(0, size - 1)
        y = random.randrange(0, size - 1)

        if (x + len(word) * direction[0] > size - 1
                or x + len(word) * direction[0] < 0
                or y + len(word) * direction[1] > size - 1
            ) or y + len(word) * direction[1] < 0:
            wordPlace(j, dictionary)
            return

        for i in range(len(word)):
            if (arr[x + direction[0] * i][y +
                                          direction[1] * i].filled == True):
                if (arr[x + direction[0] * i][y + direction[1] * i].char !=
                        word[i]):
                    wordPlace(j, dictionary)
                    return
        dictionary[j] = word

        check[j] = tk.Label(frame2,
                            text=word,
                            height=1,
                            width=15,
                            font=('None %d ' % (10)),
                            fg='#254359',
                            bg='#cbe5f7',
                            anchor='c')
        check[j].grid()

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

        if wordPressed in dictionary:
            check[int(dictionary.index(wordPressed))].configure(
                font=('Helvetica', 1), fg='#f0f0f0', bg='#f0f0f0')
            check[int(dictionary.index(wordPressed))].grid()
            dictionary[dictionary.index(wordPressed)] = ''

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
            # print(previous)
            wordPressed = arr[x][y].char
            button[x][y].configure(bg='yellow', fg='#255059')

        elif (len(wordPressed) == 1 and (x - previous[0])**2 <= 1
              and (y - previous[1])**2 <= 1 and newPressed != previous):
            wordPressed += arr[x][y].char
            button[x][y].configure(bg='yellow', fg='#255059')

            route = [x - previous[0], y - previous[1]]
            previous = [x, y]

        elif (len(wordPressed) > 1 and x - previous[0] == route[0]
              and y - previous[1] == route[1]):
            wordPressed += arr[x][y].char
            button[x][y].configure(bg='yellow', fg='#255059')
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

            button[x][y] = tk.Button(
                frame1,
                text=arr[x][y].char,
                bg='#255059',
                fg='white',
                width=2,
                height=1,
                relief=tk.FLAT,
                command=lambda x=x, y=y: buttonPress(x, y))
            button[x][y].grid(row=x, column=y)

    checkWordBtn = tk.Button(frame2,
                             text="Check Word",
                             height=1,
                             width=15,
                             anchor='c',
                             bg="#70889c",
                             font=('Helvetica', 10),
                             fg='white',
                             command=checkWord)
    checkWordBtn.grid()
