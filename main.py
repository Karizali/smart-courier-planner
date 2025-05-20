from booking_module_gui import Booking_Module_GUI
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from delivery_time_predictor_gui import open_prediction_window
from route_selection_gui import route_selection_solution




root = tk.Tk()
root.title("Smart Courier Planner - Main Menu")
root.configure(bg="lightblue")
root.geometry('500x600')

# Title Label
l0 = tk.Label(root, text="Courier System Options", font="Arial 20 bold", bg="lightblue")
l0.pack(pady=20)

# Option Buttons
bt1 = tk.Button(root, text="1. Book a Courier", font="Arial 14", bg="yellow", fg="black", width=25, command=Booking_Module_GUI)
bt1.pack(pady=10)

bt2 = tk.Button(root, text="2. Find Best Route", font="Arial 14", bg="yellow", fg="black", width=25, command=route_selection_solution)
bt2.pack(pady=10)


bt5 = tk.Button(root, text="3. Check Delivery Time", font="Arial 14", bg="yellow", fg="black", width=25, command=open_prediction_window)
bt5.pack(pady=10)

root.mainloop()