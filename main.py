import string
import tkinter as tk  # Merupakan modul untuk membuat GUI
import tkinter.messagebox as msg  # Merupakan modul untuk membuat pesan pada GUI
from tkinter import ttk  # Merupakan modul untuk membuat widget tambahan pada tkinter
import gameUtils as gutils
import Game as game
root = tk.Tk()  # Membuat objek root sebagai GUI utama
root.title("Word Search Game")

# Init


def init():
    header = tk.Frame(root)
    header.pack(fill=tk.X, side=tk.TOP)

    # FOnt bold
    heading = tk.Label(header, text="Search Me If You Can", font=(
        "Open Sans", 16, "bold"), fg='black')  # Fg = foreground merupakan warna dari text

    # Expand = True agar heading dapat mengisi seluruh ruang yang tersedia pada frame
    heading.pack(expand=True, fill=tk.X, side=tk.TOP)


def main():
    init()
    frame = tk.Frame(root)
    # padx = padding x, pady = padding y (jarak antar frame)
    frame.pack(pady=56, padx=180)

    tk.Label(frame, text="Name", font=("Open Sans", 12, "bold")).grid(
        row=0, padx=10, pady=10)
    userNameField = tk.Entry(frame, font=("Open Sans", 12))
    # ipadx = padding x, ipady = padding y (jarak antar text)
    userNameField.grid(row=0, column=1, ipadx=10, ipady=10)

    def updateUserInput():
        username = userNameField.get()
        gutils.gameLavel(levelInput.get(), username)
        if (username == ""):
            msg.showerror("Error", "Please enter your name")
        else:
            game.startGame(root)
            frame.destroy()

    tk.Label(frame, text="Game Level", font=(
        "Open Sans", 12, "bold")).grid(row=1)
    levelInput = ttk.Combobox(frame, font=("Open Sans", 12), values=[
        'Easy', 'Medium', 'Hard'])
    levelInput.grid(row=1, column=1, ipadx=10, ipady=10)

    tk.Button(frame, text="Start Game", font=("Open Sans", 12, "bold"), fg='white', bg='black', command=updateUserInput).grid(  # Command = fungsi yang akan dijalankan ketika tombol ditekan
        row=2, columnspan=2, ipadx=10, ipady=10)

    levelInput.current(0)

    root.mainloop()  # Menjalankan GUI


if __name__ == '__main__':
    main()
