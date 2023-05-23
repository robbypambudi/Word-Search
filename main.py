import string # import string
import tkinter as tk # import tkinter as tk
import tkinter.messagebox as msg # import tkinter.messagebox as msg
from tkinter import ttk # import ttk
import src.gameUtils as gutils  # import src.gameUtils as gutils
import src.Game as game # import src.Game as game

root = tk.Tk() # Membuat objek Tkinter dan menyimpannya dalam variabel root
root.title("Word Search Game") # Mengatur judul jendela aplikasi

# Init


def init():
    # menambahkan width dan height untuk membuat frame persegi
    header = tk.Frame(root, bg="white", width=600, height=200)
    header.pack(fill=tk.BOTH, side=tk.TOP)

    root.config(background='white') # Mengatur latar belakang jendela aplikasi menjadi putih

    heading = tk.Label(header, text="Search Me If You Can", font=(
        "Open Sans", 16, "bold"), fg='black', bg='white') # Membuat label judul  

    heading.pack(expand=True, fill=tk.X, side=tk.TOP) # Menempatkan label judul  di atas frame


def main():
    init() # Memanggil fungsi init() untuk menginisialisasi tampilan awal permainan
    frame = tk.Frame(root, bg="white", width=800, height=400) # Membuat frame utama dan menempatkannya di dalam root
    frame.pack(pady=56, padx=56) # Memberi jarak kosong sebesar 56 disekeliling frame 
    tk.Label(frame, text="Name", font=("Open Sans", 12, "bold"), borderwidth=0,
             highlightthickness=0, bg="white").grid(row=0, padx=10, pady=10)  # Membuat label "Name" dan menempatkannya di dalam frame
    userNameField = tk.Entry(frame, font=(
        "Open Sans", 12), bd=1, relief="solid")  # Membuat input field untuk username pemain
    userNameField.grid(row=0, column=1, padx=10, pady=10) # Menempatkan input field di sebelah kanan label "Name"

    def updateUserInput():
        username = userNameField.get() # Mendapatkan nilai username dari userNameField(input field)
        gutils.gameLavel(levelInput.get(), username) # Memanggil fungsi gameLevel dari modul gameUtils dengan level dan username sebagai argumen
        if (username == ""): # jika username kosong
            msg.showerror("Error", "Please enter your name") # Menampilkan pesan error 
        else:# jika username tidak kosong
            game.startGame(root) # Memanggil fungsi startGame dari modul Game
            frame.destroy() # Menghancurkan frame utama(frame sebelumnya)

    tk.Label(frame, text="Game Level", font=("Open Sans", 12, "bold"),
             borderwidth=0, highlightthickness=0, bg="white").grid(row=1, padx=10, pady=10)  # Membuat label "Game Level" dan menempatkannya di dalam frame
    levelInput = ttk.Combobox(frame, font=("Open Sans", 12), values=[
                              'Easy', 'Medium', 'Hard']) # Membuat combobox untuk memilih level permainan
    levelInput.grid(row=1, column=1, padx=10, pady=10) # Menempatkan combobox levelInput di sebelah kanan label "Game Level"

    tk.Button(frame, text="Start Game", font=("Open Sans", 12, "bold"), fg='white', bg='green',
              command=updateUserInput, borderwidth=0, highlightthickness=0).grid(row=2, columnspan=2, padx=10, pady=10) # Membuat tombol "Start Game" dan menempatkannya di bawah(row) input field dan combobox

    levelInput.current(0) # Mengatur pilihan level permainan ke nilai awal(Easy) 

    root.mainloop() # Memulai loop utama Tkinter


if __name__ == '__main__': # menentukan apakah script Python sedang dijalankan secara langsung (sebagai program utama) atau diimpor sebagai modul oleh skrip lain
    main() # jika skrip ini dijalankan secara langsung sebagai program utama maka fungsi main() akan dipanggil dan dieksekusi
# namun jika dipanggil sebagai modul oleh skrip lain, main() tidak akan dieksekusi secara otomatis.