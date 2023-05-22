import tkinter as tk
import tkinter.messagebox as msg
import random
from collections import deque


class Cell:
    def __init__(self, char):
        self.char = char
        self.filled = False


def isSafe(arr, x, y, visited):
    return (x >= 0 and x < len(arr) and y >= 0 and y < len(arr) and not visited[x][y])


def checkWord(arr, word, i, j, row, col, visited):
    loctemp = []
    xi, yi = i, j
    temp = 0

    while (isSafe(arr, xi, yi, visited) and arr[xi][yi].char == word[temp]):
        loctemp.append([xi, yi])
        temp += 1
        xi += row
        yi += col

        if temp == len(word):
            return {'location': loctemp, 'word': word}

    return {'location': [], 'word': []}


def dfs(arr, word, i, j, visited):
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
                    res = checkWord(
                        arr, word, x + row[k], y + col[k], row[k], col[k], visited)

                    # Compare res with word
                    w = res['word']
                    if len(w) == len(word) and all(w[i] == word[i] for i in range(len(w))):
                        return {'status': True, 'location': res['location']}

    return {'status': False, 'location': []}


def bfs(arr, word, i, j, visited):
    queue = deque()
    queue.append([i, j])
    row = [-1, -1, -1, 0, 0, 1, 1, 1]
    col = [-1, 0, 1, -1, 1, -1, 0, 1]

    while queue:
        x, y = queue.popleft()
        visited[x][y] = True

        for k in range(8):
            if isSafe(arr, x + row[k], y + col[k], visited):
                queue.append([x + row[k], y + col[k]])

                if arr[x + row[k]][y + col[k]].char == word[0]:
                    res = checkWord(
                        arr, word, x + row[k], y + col[k], row[k], col[k], visited)

                    # Compare res with word
                    w = res['word']
                    if len(w) == len(word) and all(w[i] == word[i] for i in range(len(w))):
                        return {'status': True, 'location': res['location']}

    return {'status': False, 'location': []}


def help(root: tk.Tk, arr, button, wordIndex, wordData):
    # Initialize visited arrays for DFS and BFS
    visited_dfs = [[False for _ in range(len(arr))] for _ in range(len(arr))]
    visited_bfs = [[False for _ in range(len(arr))] for _ in range(len(arr))]

    # Randomly choose a word from wordData
    data = random.choice(wordData)
    print(data)

    # DFS
    res_dfs = dfs(arr, data['WORD'], 0, 0, visited_dfs)

    # BFS
    res_bfs = bfs(arr, data['WORD'], 0, 0, visited_bfs)

    if res_dfs['status'] and res_bfs['status']:
        # Both DFS and BFS found the word
        if len(res_dfs['location']) < len(res_bfs['location']):
            # DFS found the word with fewer steps
            res = res_dfs
            markVisitedCells(res['location'], visited_bfs)
        else:
            # BFS found the word with fewer steps
            res = res_bfs
            markVisitedCells(res['location'], visited_dfs)
    elif res_dfs['status']:
        # Only DFS found the word
        res = res_dfs
        markVisitedCells(res['location'], visited_bfs)
    elif res_bfs['status']:
        # Only BFS found the word
        res = res_bfs
        markVisitedCells(res['location'], visited_dfs)
    else:
        # Neither DFS nor BFS found the word
        res = {'status': False, 'location': []}

    for i in range(len(res['location'])):
        x, y = res['location'][i]
        arr[x][y].filled = True
        button[x][y].config(bg='#2c334a', fg='#ffffff')


def markVisitedCells(locations, visited):
    for loc in locations:
        x, y = loc
        visited[x][y] = True
