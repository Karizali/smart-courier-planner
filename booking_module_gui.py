import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
import random
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import requests
import re

load_dotenv()

def generateId(min=0,max=100):
    a = random.randint(min,max)
    return a


def Booking_Module_GUI():
    
    
    api_key = os.getenv("API_KEY")
    
    root = tk.Toplevel()
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



    def is_valid_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    def validation():

        
        email = email_var.get().strip()
        contact = contact_var.get().strip()
        destination_address = destination_address_var.get().strip()
        print(item_name_var.get().strip())
        print(customer_name_var.get().strip())
        
        if any(var.get().strip() == "" for var in [
            item_name_var, 
            customer_name_var
        ]):
            messagebox.showerror("Input Error", "All fields are required and must not be empty.")
            return False

        if not is_valid_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return False

        if not contact.isdigit() or len(contact) < 10:
            messagebox.showerror("Invalid Contact Number", "Please enter a valid contact number with at least 10 digits.")
            return False
    
        if (("block" not in destination_address.lower() and "sector" not in destination_address.lower()) 
            or len(destination_address) < 10):
            messagebox.showerror("Invalid Destination Address", 
                                 "Please enter a complete destination address including house no., city, area, sector or block.")
            return False

        messagebox.showinfo("Courier Booked", f"Courier booked for: {destination_address}")
        return True

    def save_to_db():
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
        id_=generateId(1000,9999)
        
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
        ({id_}, '{item_name_var.get()}', {contact_var.get()} , 
        '{destination_address_var.get()}',
        '{branch_address_var.get()}', '{customer_name_var.get()}', '{email_var.get()}', 
        '{courier_type_var.get()}', '{city_var.get()}', '{courier_route_var.get()}', 
        '{courier_weight_var.get()}')    
        """)
        conn.commit()
        cur.close()
        conn.close()
        return id_

    def send_invoice_email(to_email, pdf_file_path):
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD") 

        msg = EmailMessage()
        msg['Subject'] = "Your Courier Invoice"
        msg['From'] = sender_email
        msg['To'] = to_email
        msg.set_content("Thank you for using our courier service. Please find your invoice attached.")

        # Read and attach PDF
        with open(pdf_file_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(pdf_file_path)

        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        messagebox.showinfo("Success", f"Data saved and invoice send to your Email: {file_name}")

    def generate_invoice_pdf(invoice_id):
        data = {
        "Invoice ID": invoice_id,
        "Item": item_name_var.get(),
        "Contact Number": contact_var.get(),
        "Destination": destination_address_var.get(),
        "Branch": branch_address_var.get(),
        "Customer Name": customer_name_var.get(),
        "Email": email_var.get(),
        "Courier Type": courier_type_var.get(),
        "City": city_var.get(),
        "Courier Route": courier_route_var.get(),
        "Courier Weight": courier_weight_var.get()
        }
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
    
        pdf.cell(200, 10, txt="Courier Invoice", ln=True, align='C')
        pdf.ln(10)
    
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
        file_name = f"Invoice_{invoice_id}.pdf"
        pdf.output(file_name)
        return file_name
    
    def save_latitude_longitude(id):
        conn= psycopg2.connect(host="localhost", dbname="postgres" ,user="postgres", password="12345", port=5432)
        cur= conn.cursor()
        
        destination_address = destination_address_var.get().split(",",1)[1]
        branch_address = branch_address_var.get().split(",",1)[1]
        
        url = f"https://graphhopper.com/api/1/geocode?q={destination_address}&locale=pk&key={api_key}"
        response = requests.get(url)
        destination_address_lat=response.json()["hits"][0]["point"]['lat']
        destination_address_lng=response.json()["hits"][0]["point"]['lng']
        url = f"https://graphhopper.com/api/1/geocode?q={branch_address}&locale=pk&key={api_key}"
        response = requests.get(url)
        branch_address_lat=response.json()["hits"][0]["point"]['lat']
        branch_address_lng=response.json()["hits"][0]["point"]['lng']
        cur.execute("""CREATE TABLE IF NOT EXISTS lat_lng (
            id INT PRIMARY KEY,
            des_lat VARCHAR(255),
            des_lng VARCHAR(255),
            br_lat VARCHAR(255),
            br_lng VARCHAR(255)
            )""")
        cur.execute(f"""INSERT INTO lat_lng (
            id ,
            des_lat,
            des_lng,
            br_lat,
            br_lng
            ) VALUES 
            ({id}, '{destination_address_lat}', 
            '{destination_address_lng}',
            '{branch_address_lat}', '{branch_address_lng}'
            )    
            """)
        conn.commit()
        cur.close()
        conn.close()
        
        

    def Submit():
        isValidation=validation()        
        if not isValidation:
            return
        try:
            id=save_to_db()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving to database: {str(e)}")
            return
        try:
            save_latitude_longitude(id)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving latitude and longitude: {str(e)}")
            return
        try:
            pdf_path=generate_invoice_pdf(id)
        except Exception as e:
            messagebox.showerror("PDF Generation Error", f"Error generating PDF: {str(e)}")
            print(f"Invoice generated: {pdf_path}")
            return
        try:
            send_invoice_email(email_var.get(), pdf_path)
        except Exception as e:
            messagebox.showerror("Email Sending Error", f"Error sending email: {str(e)}")
            return


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
    
    # Configure comboboxes to prevent empty values
    city_combo['state'] = 'readonly'
    courier_route_combo['state'] = 'readonly'
    courier_weight_combo['state'] = 'readonly'
    # Initialize radio button variable with default value
    courier_route_combo.set("Standard") 
    courier_type_var.set("City to City") 
    city_combo.set("Karachi") 
    courier_weight_combo.set("1-5 kg") 

    bt = tk.Button(
    root, 
    text="Register", 
    bg="#ffd700",             
    fg="#b22222",             
    font=("Arial", 11, "bold"),
    width=15,
    relief="raised",
    bd=2,
    command=Submit
)
    bt.pack( padx=10, pady=20)

    root.geometry('500x600')
    root.mainloop()