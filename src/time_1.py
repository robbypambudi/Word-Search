import tkinter as tk
import time


# Timer
def timer(root: tk.Tk, timeleft):
    global timeLeft
    timeLeft = timeleft

    def countdown():
        global timeLeft
        if timeLeft > 0:
            timeLeft -= 1
            minute = timeLeft // 60
            second = timeLeft % 60
            timeLabel.config(text=str(minute) + ":" + str(second) + "s")
            timeLabel.after(1000, countdown)
        else:
            timeLabel.config(text="Time's up!")
    timeLabel = tk.Label(root, text="60", font=("Open Sans", 12, "bold"))
    timeLabel.pack()
    countdown()
