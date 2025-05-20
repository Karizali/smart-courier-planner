import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from delivery_time_predictorCC import DeliveryTimePredictor
   
   

predictor = DeliveryTimePredictor()
predictor.train_model('./data_files/city_to_city_courier_rates.csv', './data_files/courier_rates.csv')

def open_prediction_window():
    

    root = tk.Toplevel()
    root.title("Order place - Smart Courier Planner")
    root.configure(bg="lightblue")

    
    # Label and Entry for ID
    tk.Label(root, text="Enter Parcel ID:", font="arial 10", bg="lightblue").pack(pady=5)
    id_var = tk.StringVar()
    tk.Entry(root, textvariable=id_var, width=25).pack(pady=5)
    
    # Text widget to display results
    result_text = tk.Text(root, height=15, width=50)
    result_text.pack(pady=10)
    
    def predict_delivery_time():
        print("Predicting delivery time...")
        try:
            conn= psycopg2.connect(host="localhost", dbname="postgres" ,user="postgres", password="12345", port=5432)
            cur= conn.cursor()
            parcel_id = int(id_var.get())
            print("sddfs",parcel_id)
            # Fetch data from database
            cur.execute(f"SELECT * FROM couriers WHERE id = {parcel_id}")
            parcel_data = cur.fetchone()
            
            if not parcel_data:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "No parcel found with this ID")
                return
            
            # Prepare data for prediction
            input_data = {
                'source_city': parcel_data[8],  # city (assuming this is destination)
                'destination_city': parcel_data[8],  # Need to adjust based on your DB structure
                'courier_type': parcel_data[7],  # courier_type
                'weight_category': parcel_data[10],  # courier_weight
                "delivery_type": parcel_data[9]
            }
            
            # Predict delivery time
            delivery_time = predictor.predict_delivery_time(input_data)
            
            # Display results
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Parcel ID: {parcel_data[0]}\n")
            result_text.insert(tk.END, f"Item: {parcel_data[1]}\n")
            result_text.insert(tk.END, f"Customer: {parcel_data[5]}\n")
            result_text.insert(tk.END, f"Source: {parcel_data[8]}\n")
            result_text.insert(tk.END, f"Destination: {parcel_data[3]}\n")
            result_text.insert(tk.END, f"Courier Type: {parcel_data[7]}\n")
            result_text.insert(tk.END, f"Weight: {parcel_data[10]}\n")
            result_text.insert(tk.END, f"\nEstimated Delivery Time: {delivery_time} days\n")
            conn.commit()
            cur.close()
            conn.close()
            
        except ValueError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Please enter a valid numeric ID")
        except Exception as e:
            print("Error:", str(e))
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Error: {str(e)}")
    
    # Prediction button
    tk.Button(
        root, 
        text="Predict Delivery Time", 
        bg="lightgreen",
        command=predict_delivery_time
    ).pack(pady=10)
    
    # Close button
    tk.Button(
        root,
        text="Close",
        bg="lightcoral",
        command=root.destroy
    ).pack(pady=5)


    root.geometry('500x600')
    root.mainloop()
    

# Add the prediction button to your main window (add this before root.mainloop())
