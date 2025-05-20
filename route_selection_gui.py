import psycopg2
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from route_selection_logic import find_best_route

def route_selection_solution():
    
    root = tk.Toplevel()
    root.title("Route Selection - Smart Courier Planner")
    root.configure(bg="lightblue")


    
    solution=find_best_route()
    print(solution)
    
    conn= psycopg2.connect(host="localhost", dbname="postgres" ,user="postgres", password="12345", port=5432)
    cur= conn.cursor()
    destination_addresses=[]
    for i in range(len(solution[1])):
        cur.execute(f"""
            SELECT destination_address FROM couriers WHERE id={solution[1][i]}
            """)
        destination_addresses.append(cur.fetchone()[0])
    
    for i in solution[0]:
        print(destination_addresses[i],"---> ",end="")
    conn.commit()
    cur.close()
    conn.close()
    
    tk.Label(
    root,
    text=f"Total Routes are: {len(destination_addresses)}",
    font=("Arial", 12, "bold"),
    bg="lightblue",
    fg="darkblue",
    padx=10,
    pady=10,
    borderwidth=2,
    relief="groove"
    ).pack(pady=10)
    
    
    def print_best_solution():
        # Label and Entry for ID


        result_text = tk.Text(
            root,
            height=15,
            width=50,
            font=("Courier New", 11),
            bg="#f0f8ff",           # Light pastel blue background
            fg="black",
            relief="sunken",
            bd=2,                   # Border width
            wrap="word",            # Wrap text at word boundaries
            padx=10,
            pady=10
        )
        result_text.pack(pady=10, fill='x', expand=True)
        

        for i in solution[0]:
            result_text.insert(tk.END, f"{destination_addresses[i]} ---> ")
        
        result_text.insert(tk.END, f"{destination_addresses[solution[0][0]]}")
        result_text.configure(state="disabled")


# Prediction button
    tk.Button(
    root, 
    text="Find Best Route", 
    bg="#90ee90",            
    fg="black",
    font=("Arial", 11, "bold"),
    width=20,
    relief="raised",
    bd=2,
    command=print_best_solution
    ).pack(pady=10)

# Close button
    tk.Button(
    root,
    text="Close",
    bg="#ff7f7f",            
    fg="black",
    font=("Arial", 11, "bold"),
    width=20,
    relief="raised",
    bd=2,
    command=root.destroy
    ).pack(pady=5)



    root.geometry('500x600')
    root.mainloop()


