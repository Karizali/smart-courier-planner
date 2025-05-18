import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def Booking_Module_GUI():
    root = tk.Tk()
    root.title("Order place - Smart Courier Planner")
    root.configure(bg="lightblue")

    item_name_var = tk.StringVar()
    contact_var = tk.StringVar()
    email_var = tk.StringVar()
    gender_var = tk.StringVar()
    city_var = tk.StringVar()
    courier_weight = tk.StringVar()
    customer_name_var = tk.StringVar()
    destination_address_var = tk.StringVar()
    branch_address_var = tk.StringVar()

    VALID_USERNAME = "kariz"

    def Submit():
        # if email_var.get():
        #     messagebox.showinfo("Invalid Email", "Please Enter correct email")
        #     return
        # if contact_var.get() =="" or not contact_var.get().isdigit() or len(contact_var.get()) < 2:
        #     messagebox.showerror("Invalid Contact Number", "Please Enter correct Contact Number")
        #     return
        if destination_address_var.get().count("block")==0 and destination_address_var.get().count("sector")==0 or len(destination_address_var.get()) < 10:
            messagebox.showerror("Invalid Destination Address", "Please Enter Complete Destination Address with house no. , city name, area name , sector/block")
            return
        else:
            messagebox.showinfo("Courier Booked", f"Courier booked for {destination_address_txt.get()}")


    l0 = tk.Label(root, text="Courier Details", font="arial 20 bold", bg="lightblue")
    l0.pack(anchor='w' ,padx=10)

    l1 = tk.Label(root, text="Item*", font="arial 10", bg="lightblue")
    l1.pack(anchor='w' ,padx=10)
    item_name_txt = tk.Entry(root, textvariable=item_name_var, width=25)
    item_name_txt.pack(anchor='w' ,padx=10)

    customer_name_label = tk.Label(root, text="Customer Name*", font="arial 10", bg="lightblue")
    customer_name_label.pack(anchor='w' ,padx=10)
    customer_name_txt = tk.Entry(root, textvariable=customer_name_var, width=25)
    customer_name_txt.pack(anchor='w' ,padx=10)

    l2 = tk.Label(root, text="Contact number*", font="arial 10", bg="lightblue")
    l2.pack(anchor='w' ,padx=10)
    contact_txt = tk.Entry(root, textvariable=contact_var, width=25)
    contact_txt.pack(anchor='w' ,padx=10)

    l3 = tk.Label(root, text="Email*", font="arial 10", bg="lightblue")
    l3.pack(anchor='w' ,padx=10)
    email_txt = tk.Entry(root, textvariable=email_var, width=25)
    email_txt.pack(anchor='w' ,padx=10)

    destination_address_label = tk.Label(root, text="Destination Address*", font="arial 10", bg="lightblue")
    destination_address_label.pack(anchor='w' ,padx=10)
    destination_address_txt = tk.Entry(root, textvariable=destination_address_var, width=25)
    destination_address_txt.pack(anchor='w' ,padx=10)

    branch_address_label = tk.Label(root, text="Branch Address*", font="arial 10", bg="lightblue")
    branch_address_label.pack(anchor='w' ,padx=10)
    branch_address_txt = tk.Entry(root, textvariable=branch_address_var, width=25)
    branch_address_txt.pack(anchor='w' ,padx=10)

    l4 = tk.Label(root, text="Courier type*", font="arial 10", bg="lightblue")
    l4.pack(anchor='w' ,padx=10)

    courier_type_frame = tk.Frame(root, bg="lightblue")
    courier_type_frame.pack(anchor='w' ,padx=10)
    rad1 = tk.Radiobutton(courier_type_frame, text="Standard", variable=gender_var, value="Standard", bg="lightblue")
    rad2 = tk.Radiobutton(courier_type_frame, text="Sentimental", variable=gender_var, value="Sentimental", bg="lightblue")
    rad3 = tk.Radiobutton(courier_type_frame, text="Business", variable=gender_var, value="Business", bg="lightblue")
    rad1.pack(side='left')
    rad2.pack(side='left')
    rad3.pack(side='left')

    l5 = tk.Label(root, text="City*", font="arial 10", bg="lightblue")
    l5.pack(anchor='w' ,padx=10)
    city_combo = ttk.Combobox(root, textvariable=city_var)
    city_combo['values'] = ("Lahore", "Karachi", "Peshawar", "Quetta", "Islamabad")
    city_combo.pack(anchor='w' ,padx=10)

    l6 = tk.Label(root, text="Courier Weight*", font="arial 10", bg="lightblue")
    l6.pack(anchor='w' ,padx=10)
    courier_weight_combo = ttk.Combobox(root, textvariable=courier_weight)
    courier_weight_combo['values'] = ("1-5 kg", "5-10 kg", "10-20 kg", "20-50 kg", "50+ kg")
    courier_weight_combo.pack(anchor='w' ,padx=10)

    bt = tk.Button(root, text="Register", bg="yellow", fg="red", command=Submit)
    bt.pack(anchor='w' ,padx=10)

    root.geometry('500x600')
    root.mainloop()
