import tkinter as tk
import gameUtils as gutils


def startGame(root):
    frame1 = tk.Frame(master=root, bg="red")
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=20, pady=20)

    frame2 = tk.Frame(master=root)
    frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=12)

    config = gutils.readConfigFile()

    level = config['player']['level']
    levelDetails = [
        config['levels'][level]['name'],
        config['levels'][level]['words'],
    ]

    currScore = tk.StringVar()
    currScore.set(0)

    frame3 = tk.Frame(master=root)
    frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=12)
