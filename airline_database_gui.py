import tkinter as tk
from tkinter import messagebox

import pymysql

# GUI setup

root = tk.Tk()
root.title("Flight Tracker Database")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

# Starting screen
welcome_frame = tk.Frame(root, bg="#f0f0f0")
welcome_frame.pack(expand=True, fill="both")

# Procedures dashboard
dashboard_frame = None

title_label = tk.Label(
    welcome_frame,
    text="Welcome to Flight Tracker",
    font=("Helvetica", 24, "bold"),
    bg="#f0f0f0",
    fg="#333"
)
title_label.pack(pady=30)

desc_label = tk.Label(
    welcome_frame,
    text="Manage flights, track status, and view records easily.\nUse the menu or buttons below to get started.",
    font=("Helvetica", 14),
    bg = "#f0f0f0",
    fg="#000"
)
desc_label.pack(pady=10)

def test_connection():
    try:
        connection = connect()
        connection.close()
        messagebox.showinfo("Connection Status", "Successfully connected to MySQL!")
    
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect:\n{e}")
        
def connect():
    return pymysql.connect (
            host = "localhost",
            port = 3306,
            user = "root",
            password = "*****", #insert your password here! Make sure to remove password when committing
            database = "flight_tracking"
        )

def execute_procedure(proc_name):
    try:
        conn = connect()
        with conn.cursor() as cursor:
            cursor.callproc(proc_name)
        conn.commit()
        messagebox.showinfo("Success", f"Procedure '{proc_name}' executed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute '{proc_name}':\n{e}")
    finally:
        conn.close()

def go_to_dashboard():
    global dashboard_frame
    # Reset frame
    welcome_frame.pack_forget()
    
    dashboard_frame = tk.Frame(root, bg="#e6f2ff")
    dashboard_frame.pack(expand=True, fill="both")

    tk.Label(
        dashboard_frame,
        text="Stored Procedure Dashboard",
        font=("Helvetica", 20, "bold"),
        bg="#e6f2ff"
    ).pack(pady=20)

    # Buttons
    button_frame = tk.Frame(dashboard_frame, bg="#e6f2ff")
    button_frame.pack(pady=20)
    
    procedures = {
        "add_airplane" : add_airplane_page
    }
    
    incomplete = [
        "add_airport", 
        "add_person", 
        "grant_or_revoke_pilot_license", 
        "offer_flight", "flight_landing", 
        "flight_takeoff", "passengers_board", 
        "passengers_disembark",
        "assign_pilot", 
        "recycle_crew", 
        "retire_flight", 
        "simulation_cycle"
    ]
    
    for idx, (proc, func) in enumerate(procedures.items()):
        tk.Button(
            button_frame,
            text=proc.replace("_", " ").title(),
            width=30,
            command=func
        ).grid(row=idx // 2, column=idx % 2, padx=10, pady=5)

def add_airplane_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    form_frame = tk.Frame(root, bg="#e6ffe6")
    form_frame.pack(expand=True, fill="both")

    tk.Label(form_frame, text="Add Airplane", font=("Helvetica", 20, "bold"), bg="#e6ffe6").pack(pady=20)

    labels = ["Airplane ID", "Model", "Capacity"]
    entries = []

    for label in labels:
        frame = tk.Frame(form_frame, bg="#e6ffe6")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#e6ffe6").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
    
def clean_exit():
    root.destroy()

# Welcome buttons
button_frame = tk.Frame(welcome_frame, bg="#f0f0f0")
button_frame.pack(pady=30)

tk.Button(button_frame, text="Procedures Dashboard", width=20, command=go_to_dashboard).grid(row=0, column=0, padx=10, pady=10)
tk.Button(button_frame, text="Connections Test", width=20, command=test_connection).grid(row=0, column=1, padx=10, pady=10)
tk.Button(button_frame, text="Exit", width=20, command=clean_exit).grid(row=0, column=2, padx=10, pady=10)

# Create window

root.mainloop()



