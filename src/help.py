import tkinter as tk
import tkinter.messagebox as msg
import random


def isSafe(arr, x, y, visited):
    return (x >= 0 and x < len(arr) and y >= 0 and y < len(arr) and not visited[x][y])


def checkWordUtil(arr, word, i, j, row, col, visited):
    loctemp = []
    xi, yi = i, j
    temp = 0
    while (isSafe(arr, xi, yi, visited) and arr[xi][yi].char == word[temp]):
        loctemp.append([xi, yi])
        temp += 1
        xi += row
        yi += col
        if temp == len(word):
            return {'location': loctemp, 'word': word, 'status': True}

    return {'location': [], 'word': [], 'status': False}


def checkWord(arr, word, i, j):
    visited = [[False for i in range(len(arr))] for j in range(len(arr))]
    row = [-1, -1, -1, 0, 0, 1, 1, 1]
    col = [-1, 0, 1, -1, 1, -1, 0, 1]

    for direction in range(8):
        res = checkWordUtil(
            arr, word, i, j, row[direction], col[direction], visited)
        if res['status']:
            return res
    return {'location': [], 'word': [], 'status': False}


def dfs(arr, word, i, j):
    visited = [[False for i in range(len(arr))] for j in range(len(arr))]
    stack = []
    stack.append([i, j])
    row = [-1, -1, -1, 0, 0, 1, 1, 1]
    col = [-1, 0, 1, -1, 1, -1, 0, 1]

    while stack:
        x, y = stack.pop()
        visited[x][y] = True
        for k in range(8):
            if isSafe(arr, x + row[k], y + col[k], visited):
                stack.append([x + row[k], y + col[k]])
                if arr[x + row[k]][y + col[k]].char == word[0]:

                    res = checkWord(arr, word, x + row[k], y + col[k])
                    # Compare res with word
                    w = res['word']
                    if (len(w) == len(word)):
                        for i in range(len(w)):
                            if w[i] != word[i]:
                                return {'status': False, 'location': []}
                        return {'status': True, 'location': res['location']}

    return {'status': False, 'location': []}


def help(root: tk.Tk, arr, button, wordList, wordData):
    global location

    i = 0
    word = random.choice(wordList)
    while (True):

        if (not word["IS_HELPED"]):
            word["IS_HELPED"] = True
            break
        i += 1
        if (i == len(wordList)):
            msg.showinfo("Help", "No more words to help")
            return

        word = random.choice(wordList)

    res = dfs(arr, word["WORD"], 0, 0)

    for i in range(len(res['location'])):
        x, y = res['location'][i]
        arr[x][y].filled = True
        button[x][y].config(bg='#2c334a', fg='#ffffff')
