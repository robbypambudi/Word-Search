import tkinter as tk
import tkinter.messagebox as msg
import random

import src.gameUtils as gutils

def isSafe(arr, x, y, visited):
    return (x >= 0 and x < len(arr) and y >= 0 and y < len(arr) and not visited[x][y]) # Cek apakah x dan y berada dalam range array dan belum dikunjungi


def checkWordUtil(arr, word, i, j, row, col, visited):
    loctemp = [] # Membuat list kosong untuk menampung lokasi kata
    xi, yi = i, j # Mendefinisikan xi dan yi dengan nilai i dan j
    temp = 0 # Mendefinisikan temp dengan nilai 0
    while (isSafe(arr, xi, yi, visited) and arr[xi][yi].char == word[temp]): # Selama x dan y berada dalam range array dan belum dikunjungi dan karakter pada array sama dengan karakter pada kata
        loctemp.append([xi, yi]) # Menambahkan lokasi x dan y pada list loctemp
        temp += 1 # Menambahkan nilai temp dengan 1
        xi += row # Menambahkan nilai xi dengan row
        yi += col # Menambahkan nilai yi dengan col
        if temp == len(word): # Jika temp sama dengan panjang kata maka kata ditemukan
            return {'location': loctemp, 'word': word, 'status': True}

    return {'location': [], 'word': [], 'status': False} # Jika kata tidak ditemukan maka mengembalikan nilai False


def checkWord(arr, word, i, j):
    visited = [[False for i in range(len(arr))] for j in range(len(arr))] # Membuat array 2 dimensi dengan ukuran array
    row = [-1, -1, -1, 0, 0, 1, 1, 1] # Mendefinisikan row dengan array 1 dimensi digunakan untuk menentukan arah
    col = [-1, 0, 1, -1, 1, -1, 0, 1] # Mendefinisikan col dengan array 1 dimensi digunakan untuk menentukan arah

    for direction in range(8): # Melakukan perulangan sebanyak 8 kali
        res = checkWordUtil(
            arr, word, i, j, row[direction], col[direction], visited) # Memanggil fungsi checkWordUtil dengan parameter array, kata, i, j, row, col, dan visited
        if res['status']: # Jika status True maka kata ditemukan
            return res # Mengembalikan nilai res
    return {'location': [], 'word': [], 'status': False} # Jika kata tidak ditemukan maka mengembalikan nilai False


def dfs(arr, word, i, j):
    visited = [[False for i in range(len(arr))] for j in range(len(arr))] # Membuat array 2 dimensi dengan ukuran array
    stack = [] # Membuat list kosong untuk menampung lokasi kata
    stack.append([i, j]) # Menambahkan lokasi i dan j pada list stack
    row = [-1, -1, -1, 0, 0, 1, 1, 1] # Mendefinisikan row dengan array 1 dimensi digunakan untuk menentukan arah
    col = [-1, 0, 1, -1, 1, -1, 0, 1] # Mendefinisikan col dengan array 1 dimensi digunakan untuk menentukan arah

    while stack:
        x, y = stack.pop() # Menghapus elemen terakhir pada list stack dan menyimpannya pada variabel x dan y
        visited[x][y] = True # Mengubah nilai visited pada x dan y menjadi True
        for k in range(8):
            if isSafe(arr, x + row[k], y + col[k], visited): # Jika x dan y berada dalam range array dan belum dikunjungi
                stack.append([x + row[k], y + col[k]]) # Menambahkan lokasi x dan y pada list stack
                if arr[x + row[k]][y + col[k]].char == word[0]: # Jika karakter pada array sama dengan karakter pada kata

                    res = checkWord(arr, word, x + row[k], y + col[k]) # Memanggil fungsi checkWord dengan parameter array, kata, x + row[k], dan y + col[k]
                    # Compare res with word
                    w = res['word'] # Mendefinisikan w dengan nilai res['word']
                    if (len(w) == len(word)): # Jika panjang w sama dengan panjang kata
                        for i in range(len(w)): # Melakukan perulangan sebanyak panjang w
                            if w[i] != word[i]: # Jika karakter pada w tidak sama dengan karakter pada kata
                                return {'status': False, 'location': []} # Mengembalikan nilai False
                        return {'status': True, 'location': res['location']} # Mengembalikan nilai True dan lokasi kata

    return {'status': False, 'location': []}

def checkScore(): # Cek apakah score masih lebih dari 0
    config = gutils.readConfigFile()
    score = config['player']['score']
    if (score <= 0):
        return False
    return True
    


def help(root: tk.Tk, arr, button, wordList, updateScore):
    global location

    i = 0
    word = random.choice(wordList) # Memilih kata secara random
    while (True):   # Memilih kata yang belum dihelp

        if (not word["IS_HELPED"]): # Jika kata belum dihelp
            word["IS_HELPED"] = True # Mengubah nilai IS_HELPED menjadi True
            break
        i += 1
        if (i == len(wordList)): # Jika semua kata sudah dihelp
            msg.showinfo("Help", "No more words to help") # Menampilkan pesan no more words to help
            return

        word = random.choice(wordList) # Memilih kata secara random

    #output bantuan saat belum ada nilai
    if (not checkScore()):
        msg.showinfo("Maaf!", "Jangan Bantuan terus abang LOL")
        return   
     
    res = dfs(arr, word["WORD"], 0, 0) # Memanggil fungsi dfs dengan parameter array, kata, 0, dan 0
    updateScore(-8)

    for i in range(len(res['location'])):
        x, y = res['location'][i]
        arr[x][y].filled = True
        button[x][y].config(bg='yellow', fg='black')
