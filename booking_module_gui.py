import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
import random

def generateId(min=0,max=100):
    a = random.randint(min,max)
    return a
def Booking_Module_GUI():
    
    conn= psycopg2.connect(host="localhost", dbname="postgres" ,user="postgres", password="12345", port=5432)
    cur= conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS couriers (
        id INT PRIMARY KEY,
        item VARCHAR(255),
        contact_num VARCHAR(255),
        destination_address VARCHAR(255),
        branch_address VARCHAR(255),
        customer_name VARCHAR(255),
        email VARCHAR(255),
        courier_type VARCHAR(255),
        city VARCHAR(255),
        courier_route VARCHAR(255),
        courier_weight VARCHAR(255)
        )""")
    
    
    
    
    root = tk.Tk()
    root.title("Order place - Smart Courier Planner")
    root.configure(bg="lightblue")

    item_name_var = tk.StringVar()
    contact_var = tk.StringVar()
    email_var = tk.StringVar()
    courier_route_var = tk.StringVar()
    city_var = tk.StringVar()
    courier_weight_var = tk.StringVar()
    customer_name_var = tk.StringVar()
    destination_address_var = tk.StringVar()
    branch_address_var = tk.StringVar()
    courier_type_var = tk.StringVar()


    def Submit():
        # if email_var.get():
        #     messagebox.showinfo("Invalid Email", "Please Enter correct email")
        #     return
        # if contact_var.get() =="" or not contact_var.get().isdigit() or len(contact_var.get()) < 2:
        #     messagebox.showerror("Invalid Contact Number", "Please Enter correct Contact Number")
        #     return
        # if destination_address_var.get().count("block")==0 and destination_address_var.get().count("sector")==0 or len(destination_address_var.get()) < 10:
        #     messagebox.showerror("Invalid Destination Address", "Please Enter Complete Destination Address with house no. , city name, area name , sector/block")
        #     return
        # else:
        #     messagebox.showinfo("Courier Booked", f"Courier booked for {destination_address_txt.get()}")
        #     cur.execute(f"""INSERT INTO couriers (
        #         id ,
        #         name ,
        #         contact_num ,
        #         destination_address,
        #         branch_address
        #         ) VALUES 
        #         (1, 'Ali', 1234567890, 'House No. 123, Sector 5, Lahore', 'Branch No. 456, Block A, Lahore')
        #         """)
        
        
        cur.execute(f"""INSERT INTO couriers (
                id ,
                item ,
                contact_num ,
                destination_address,
                branch_address,
                customer_name,
                email,
                courier_type,
                city,
                courier_route,
                courier_weight
                ) VALUES 
                ({generateId(1000,9999)}, '{item_name_var.get()}', {contact_var.get()} , 
                '{destination_address_var.get()}',
                '{branch_address_var.get()}', '{customer_name_var.get()}', '{email_var.get()}', 
                '{courier_type_var.get()}', '{city_var.get()}', '{courier_route_var.get()}', 
                '{courier_weight_var.get()}')    
                """)


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
    rad1 = tk.Radiobutton(courier_type_frame, text="Standard", variable=courier_type_var, value="Standard", bg="lightblue")
    rad2 = tk.Radiobutton(courier_type_frame, text="Sentimental", variable=courier_type_var, value="Sentimental", bg="lightblue")
    rad3 = tk.Radiobutton(courier_type_frame, text="Business", variable=courier_type_var, value="Business", bg="lightblue")
    rad1.pack(side='left')
    rad2.pack(side='left')
    rad3.pack(side='left')

    l5 = tk.Label(root, text="City*", font="arial 10", bg="lightblue")
    l5.pack(anchor='w' ,padx=10)
    city_combo = ttk.Combobox(root, textvariable=city_var)
    city_combo['values'] = ("Lahore", "Karachi", "Peshawar", "Quetta", "Islamabad")
    city_combo.pack(anchor='w' ,padx=10)
    
    courier_route_label = tk.Label(root, text="Courier Route*", font="arial 10", bg="lightblue")
    courier_route_label.pack(anchor='w' ,padx=10)
    courier_route_combo = ttk.Combobox(root, textvariable=courier_route_var)
    courier_route_combo['values'] = ("City to City", "within same city")
    courier_route_combo.pack(anchor='w' ,padx=10)

    l6 = tk.Label(root, text="Courier Weight*", font="arial 10", bg="lightblue")
    l6.pack(anchor='w' ,padx=10)
    courier_weight_combo = ttk.Combobox(root, textvariable=courier_weight_var)
    courier_weight_combo['values'] = ("1-5 kg", "5-10 kg", "10-20 kg", "20-50 kg", "50+ kg")
    courier_weight_combo.pack(anchor='w' ,padx=10)

    bt = tk.Button(root, text="Register", bg="yellow", fg="red", command=Submit)
    bt.pack(anchor='w' ,padx=10)

    root.geometry('500x600')
    root.mainloop()
    
    
    
    conn.commit()
    cur.close()
    conn.close()
