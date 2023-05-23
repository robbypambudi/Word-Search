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
    config = gutils.readConfigFile() #  Mengambil data dari file config.yaml
    levelNum = config['player']['level'] # Mengambil level yang sedang dimainkan

    # Timer Frame
    frame = tk.Frame(root, bg="white", width=400, height=100) # Membuat frame untuk timer dan score
    frame.pack(fill=tk.BOTH, side=tk.TOP) # Mengatur posisi frame
    t.timer(frame, config['levels'][levelNum]['time']) # Memulai timer

    # Vertical Frame
    frame1 = tk.Frame(master=root, bg="red") # Membuat frame untuk grid dan tombol
    frame1.pack(side=tk.LEFT, expand=True, padx=20, pady=20) 
    frame1.grid_columnconfigure(0, weight=1)

    levelDetails = [
        config['levels'][levelNum]['name'],
        config['levels'][levelNum]['words']
    ] # Menyimpan data level yang sedang dimainkan
    currScore = tk.StringVar() # Menyimpan score yang sedang dimainkan
    currScore.set(0) # Mengatur score awal menjadi 0

    def updateScore(value): # Mengupdate score
        config = gutils.readConfigFile() # Membaca file config.yaml
        score = config['player']['score'] # Mengambil score yang sedang dimainkan
        config['player']['score'] = score + value # Menambahkan score yang sedang dimainkan dengan value
        currScore.set(score +value) # Mengupdate score yang sedang dimainkan
        gutils.writeConfigFile(config) # Menulis file config.yaml
        root.update_idletasks() # Mengupdate tampilan root (GUI)

    frame3 = tk.Frame(master=root)
    frame3.pack(fill=tk.BOTH, side=tk.RIGHT, padx=20, pady=30)

    frame4 = tk.Frame(master=root, bg='#cbe5f7', width=400)
    frame4.pack(fill=tk.BOTH, side=tk.TOP, pady=10, anchor='ne', expand=True)

    gutils.labelGame(frame3, config, levelDetails, currScore) # Membuat label untuk level dan score

    wordList = [] # Menyimpan kata-kata yang akan dimainkan

    with open(r'data/words.yaml') as file: # Membaca file words.yaml
        wordFile = yaml.load(file, Loader=yaml.FullLoader) # Mengambil data dari file words.yaml
        wordData = wordFile['words'] # Menyimpan data dari file words.yaml
        wordList = [word for word in wordFile['words']] # Menyimpan kata-kata yang akan dimainkan
        
    curLevel = config['player']['level'] # Mengambil level yang sedang dimainkan
    numWords= size = config['levels'][curLevel]['words'] # Mengambil jumlah kata yang akan dimainkan
        
        

    arr = [[0 for x in range(size)] for y in range(size)] # Membuat array 2 dimensi dengan ukuran size x size digunakan untuk menyimpan huruf yang akan dimainkan
    button = [[0 for x in range(size)] for y in range(size)] # Membuat array 2 dimensi dengan ukuran size x size digunakan untuk membuat grid
    check = [0 for numWords in range(size)] # Membuat array dengan ukuran size x size digunakan untuk mengecek apakah kata sudah ditemukan atau belum
    dictionary = [0 for createWordSet in range(numWords)] # Membuat array dengan ukuran numWords x numWords digunakan untuk menyimpan kata-kata yang akan dimainkan

    directionArr = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1],
                    [0, -1], [1, -1]]  # Membuat array 2 dimensi dengan ukuran 8 x 2 digunakan untuk menentukan arah kata yang akan dimainkan

    def handleButtonHelp():
        h.help(root, arr, button, dictionary, updateScore) # Memanggil fungsi help dari file help.py

    def nextLevel():
        config = gutils.readConfigFile() # Membaca file config.yaml
        config['player']['level'] = config['player']['level'] + 1 # Menambahkan level yang sedang dimainkan dengan 1
        gutils.writeConfigFile(config)  # Menulis file config.yaml
        frame.destroy() # Menghapus frame
        frame1.destroy() # Menghapus frame
        frame4.destroy() # Menghapus frame
        frame3.destroy() # Menghapus frame
        if (config['player']['level'] == 4): # Jika level yang sedang dimainkan adalah level 4
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

            

        else:
            startGame(root)
            root.update_idletasks()

    tk.Button(frame, text="Bantuan", font=("Open Sans", 12), fg='black', bg='yellow',
              borderwidth=0, highlightthickness=0, command=handleButtonHelp).pack(side=tk.RIGHT, padx=10)

    tk.Button(frame, text="Next Level", font=("Open Sans", 12), fg='black', bg='#4169E1',
              borderwidth=0, highlightthickness=0, command=nextLevel).pack(side=tk.LEFT, padx=10)

    class Square:
        status = False
        filled = False
        char = ''

    def fill(x, y, word, direction): # Mengisi array arr dengan kata yang akan dimainkan
        w = wordData[word]['WORD']
        for i in range(len(w)): # Mengisi array arr dengan kata yang akan dimainkan
            arr[x + direction[0] * i][y + direction[1] * i].char = w[i] # Mengisi array arr dengan kata yang akan dimainkan
            arr[x + direction[0] * i][y + direction[1] * i].filled = True # Mengisi array arr dengan kata yang akan dimainkan
        wordList.remove(word) # Menghapus kata yang sudah dimainkan dari array wordList

    def wordPlace(j, dictionary):
        word = random.choice(wordList) # Memilih kata secara acak dari array wordList
        direction = directionArr[random.randrange(0, 7)] # Memilih arah secara acak dari array directionArr
        oneWord = wordData[word]['WORD'] # Mengambil kata yang akan dimainkan
        x = random.randrange(0, size - 1) # Memilih posisi x secara acak
        y = random.randrange(0, size - 1) # Memilih posisi y secara acak

        if (x + len(oneWord) * direction[0] > size - 1 # Jika kata yang akan dimainkan melebihi ukuran array arr
                or x + len(oneWord) * direction[0] < 0 # Jika kata yang akan dimainkan melebihi ukuran array arr
                or y + len(oneWord) * direction[1] > size - 1 # Jika kata yang akan dimainkan melebihi ukuran array arr
            ) or y + len(oneWord) * direction[1] < 0: # Jika kata yang akan dimainkan melebihi ukuran array arr
            wordPlace(j, dictionary) # Memanggil fungsi wordPlace
            return

        for i in range(len(oneWord)): # Mengecek apakah kata yang akan dimainkan sudah ada di array arr
            if (arr[x + direction[0] * i][y + 
                                          direction[1] * i].filled == True): # Jika kata yang akan dimainkan sudah ada di array arr 
                if (arr[x + direction[0] * i][y + direction[1] * i].char != 
                        oneWord[i]): # Lalu jika kata yang akan dimainkan tidak sama dengan kata yang sudah ada di array arr 
                    wordPlace(j, dictionary) # Memanggil fungsi wordPlace
                    return
                
        dictionary[j] = {
            'WORD': oneWord,
            'HINT': wordData[word]['HINT'],
            'IS_HELPED': False,
        } # Menambahkan kata yang akan dimainkan ke dalam array dictionary

        check[j] = tk.Label(frame4,
                            text=wordData[word]['HINT'],
                            height=1,
                            width=50,
                            font=('None %d ' % (10)),
                            fg='#254359',
                            bg='#cbe5f7',
                            anchor='c')
        check[j].grid(row=j+1, column=0, padx=3, pady=2) # Menampilkan hint dari kata yang akan dimainkan

        fill(x, y, word, direction) # Memanggil fungsi fill
        return dictionary # Mengembalikan array dictionary

    def colourWord(wordPressed, valid): # Mengubah warna dari kata yang sudah dimainkan menjadi biru
        route[0] *= -1   # Mengubah arah kata yang akan dimainkan
        route[1] *= -1  # Mengubah arah kata yang akan dimainkan
        for i in range(len(wordPressed)): # Mengubah warna dari kata yang sudah dimainkan menjadi biru
            if valid == True or arr[previous[0] + 
                                    i * route[0]][previous[1] +
                                                  i * route[1]].status == True: # Jika kata yang dimainkan benar atau kata yang dimainkan sudah dimainkan sebelumnya
                button[previous[0] + i * route[0]][previous[1] +
                                                   i * route[1]].config(
                                                       bg='#535edb',
                                                       fg='white')
                arr[previous[0] + i * route[0]][previous[1] +
                                                i * route[1]].status = True # Mengubah status dari kata yang dimainkan menjadi True
            elif (arr[previous[0] +
                      i * route[0]][previous[1] +
                                    i * route[1]].status == False): # Jika kata yang dimainkan salah dan kata yang dimainkan belum dimainkan sebelumnya
                button[previous[0] + i * route[0]][previous[1] +
                                                   i * route[1]].config(
                                                       bg='#255059',
                                                       fg='white') # Mengubah warna dari kata yang dimainkan menjadi merah  

    def checkWord():
        global wordPressed # Mengambil kata yang dimainkan
        dict = [dictionary[i]['WORD'] 
                for i in range(len(dictionary)) if dictionary[i] != ''] # Mengambil kata yang akan dimainkan dari array dictionary

        if wordPressed in dict and wordPressed != '':
            check[int(dict.index(wordPressed))].configure(
                font=('Helvetica', 10),  fg='green',
                bg='#cbe5f7',) # Mengubah warna hint dari kata yang dimainkan menjadi hijau 

            updateScore(10) # Memanggil fungsi updateScore dengan parameter 10
            colourWord(wordPressed, True)
        else:
            colourWord(wordPressed, False) # Memanggil fungsi colourWord dengan parameter False
        wordPressed = ''
        previous = [0, 0]

    def buttonPress(x, y): # Mengubah warna dari kata yang dimainkan menjadi biru
        global wordPressed, previous, route # Mengambil kata yang dimainkan, posisi sebelumnya, dan arah kata yang akan dimainkan
        newPressed = [x, y] # Mengambil posisi dari kata yang dimainkan

        if (len(wordPressed) == 0): # Jika kata yang dimainkan belum ada
            previous = newPressed # Mengubah posisi sebelumnya menjadi posisi kata yang dimainkan
            wordPressed = arr[x][y].char # Mengambil kata yang dimainkan
            button[x][y].configure(bg='#2c334a', fg='white') # Mengubah warna dari kata yang dimainkan menjadi biru

        elif (len(wordPressed) == 1 and (x - previous[0])**2 <= 1
              and (y - previous[1])**2 <= 1 and newPressed != previous): # Jika kata yang dimainkan hanya satu dan posisi kata yang dimainkan bersebelahan dengan posisi sebelumnya
            wordPressed += arr[x][y].char # Mengambil kata yang dimainkan
            button[x][y].configure(bg='#2c334a', fg='white') # Mengubah warna dari kata yang dimainkan menjadi biru

            route = [x - previous[0], y - previous[1]] # Mengubah arah kata yang akan dimainkan
            previous = [x, y] # Mengubah posisi sebelumnya menjadi posisi kata yang dimainkan

        elif (len(wordPressed) > 1 and x - previous[0] == route[0]
              and y - previous[1] == route[1]): # Jika kata yang dimainkan lebih dari satu dan posisi kata yang dimainkan bersebelahan dengan posisi sebelumnya
            wordPressed += arr[x][y].char # Mengambil kata yang dimainkan
            button[x][y].configure(bg='#2c334a', fg='white') # Mengubah warna dari kata yang dimainkan menjadi biru
            previous = [x, y] # Mengubah posisi sebelumnya menjadi posisi kata yang dimainkan

    for x in range(size): # Membuat grid
        for y in range(size): # Membuat grid
            arr[x][y] = Square() # Membuat grid

    for i in range(numWords):
        wordPlace(i, dictionary) # Memanggil fungsi wordPlace

    for y in range(size):
        for x in range(size):

            if (arr[x][y].filled == False):
                arr[x][y].char = random.choice(string.ascii_uppercase) # Mengisi grid dengan huruf acak

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
            button[x][y].grid(row=x, column=y) # Membuat grid dengan huruf acak dan memanggil fungsi buttonPress

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
