import tkinter as tk
import threading











def my_function():

        print("Hello World!")


root = tk.Tk()

start_button = tk.Button(root, text="Start", command=start)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.pack()

root.mainloop()
