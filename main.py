import string
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk
import src.gameUtils as gutils
import src.Game as game

root = tk.Tk()
root.title("Word Search Game")

# Init


def init():
    # menambahkan width dan height untuk membuat frame persegi
    header = tk.Frame(root, bg="white", width=400, height=100)
    header.pack(fill=tk.BOTH, side=tk.TOP)

    root.config(background='white')

    heading = tk.Label(header, text="Search Me If You Can", font=(
        "Open Sans", 16, "bold"), fg='black', bg='white')

    heading.pack(expand=True, fill=tk.X, side=tk.TOP)


def main():
    init()
    frame = tk.Frame(root, bg="white", width=400, height=400)
    frame.pack(pady=56, padx=56)

    tk.Label(frame, text="Name", font=("Open Sans", 12, "bold"), borderwidth=0,
             highlightthickness=0, bg="white").grid(row=0, padx=10, pady=10)
    userNameField = tk.Entry(frame, font=(
        "Open Sans", 12), bd=1, relief="solid")
    userNameField.grid(row=0, column=1, padx=10, pady=10)

    def updateUserInput():
        username = userNameField.get()
        gutils.gameLavel(levelInput.get(), username)
        if (username == ""):
            msg.showerror("Error", "Please enter your name")
        else:
            game.startGame(root)
            frame.destroy()

    tk.Label(frame, text="Game Level", font=("Open Sans", 12, "bold"),
             borderwidth=0, highlightthickness=0, bg="white").grid(row=1, padx=10, pady=10)
    levelInput = ttk.Combobox(frame, font=("Open Sans", 12), values=[
                              'Easy', 'Medium', 'Hard'])
    levelInput.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(frame, text="Start Game", font=("Open Sans", 12, "bold"), fg='white', bg='green',
              command=updateUserInput, borderwidth=0, highlightthickness=0).grid(row=2, columnspan=2, padx=10, pady=10)

    levelInput.current(0)

    root.mainloop()


if __name__ == '__main__':
    main()
