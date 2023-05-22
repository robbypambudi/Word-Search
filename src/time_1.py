import tkinter as tk  # import tkinter as tk
import time  # import time

# Timer


def timer(root: tk.Tk, timeleft):  # mendefinisikan fungsi timer dengan parameter root dan timeleft
    global timeLeft  # mendefinisikan variabel global timeLeft
    timeLeft = timeleft  # mengisi variabel global timeLeft dengan parameter timeleft

    def countdown():  # mendefinisikan fungsi countdown
        global timeLeft  # mendefinisikan variabel global timeLeft
        if timeLeft > 0:  # jika timeLeft lebih dari 0
            timeLeft -= 1  # timeLeft dikurangi 1
            minute = timeLeft // 60  # menentukan menit (hasil bulat kebawah)
            second = timeLeft % 60  # menentukan detik (sisa bagi)
            # mengonfigurasi teks pada timeLabel untuk menampilkan menit:detik
            timeLabel.config(text=str(minute) + ":" + str(second) + "s")
            # mengatur waktu tunggu 1000 milidetik untuk menjalankan fungsi countdown
            timeLabel.after(1000, countdown)
        else:  # jika timeLeft tidak lebih dari 0
            # mengonfigurasi teks pada timeLabel untuk menampilkan Time's up!
            timeLabel.config(text="Time's up!")
    # mendefinisikan timeLabel dengan teks 60 dan font Open Sans 12 bold
    timeLabel = tk.Label(root, text="60", font=("Open Sans", 12, "bold"))
    # Menempatkan label timeLabel di dalam window utama (root) menggunakan metode pack()
    timeLabel.pack()
    countdown()  # menjalankan fungsi countdown
