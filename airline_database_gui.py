import tkinter as tk
from tkinter import messagebox

import pymysql

# GUI setup

root = tk.Tk()
root.title("Flight Tracker Database")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

# Welcome frame
welcome_frame = tk.Frame(root, bg="#f0f0f0")
welcome_frame.pack(expand=True, fill="both")

# Additional frames
dashboard_frame = None
form_frame = None
category_frame = None
person_frame = None
person_form_frame = None

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
            password = "2414510759/Aa", #insert your password here! Make sure to remove password when committing
            database = "flight_tracking"
        )

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
        "add_airplane" : add_airplane_page,
        "add_airport" : add_airport_page,
        "add_person" : add_person_page
    }
    
    incomplete = [
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
    
    tk.Button(
        dashboard_frame,
        text="Back",
        command=lambda: [dashboard_frame.pack_forget(), welcome_frame.pack(expand=True, fill="both")]
    ).pack(pady=10)


# add_airplane() setup
def add_airplane_page():
    global dashboard_frame
    global category_frame
    dashboard_frame.pack_forget()
    
    category_frame = tk.Frame(root, bg="#e6ffe6")
    category_frame.pack(expand=True, fill="both")

    tk.Label(
        category_frame,
        text="Select Airplane Type",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    tk.Button(
        category_frame,
        text="Add Boeing",
        width=30,
        command=lambda: [category_frame.pack_forget(), add_airplane_form(category_frame, "boeing")]
    ).pack(pady=10)

    tk.Button(
        category_frame,
        text="Add Airbus",
        width=30,
        command=lambda: [category_frame.pack_forget(), add_airplane_form(category_frame, "airbus")]
    ).pack(pady=10)

    tk.Button(
        category_frame,
        text="Add General",
        width=30,
        command=lambda: [category_frame.pack_forget(), add_airplane_form(category_frame, "general")]
    ).pack(pady=10)

    tk.Button(
        category_frame,
        text="Back",
        command=lambda: [category_frame.pack_forget(), dashboard_frame.pack(expand=True, fill="both")]
    ).pack(pady=20)

def add_airplane_form(prev_frame, plane_type):
    global form_frame
    form_frame = tk.Frame(root, bg="#dff0ff")
    form_frame.pack(expand=True, fill="both")

    # Boeing button
    if plane_type == "boeing":
        tk.Label(form_frame, text="Add Boeing Airplane", font=("Helvetica", 20, "bold"), bg="#dff0ff").pack(pady=20)

        labels = ["Airline ID", "Tail Number", "Seat Capacity", "Speed", "Location ID", "Maintenanced", "Model"]
        entries = []

        for label in labels:
            
            frame = tk.Frame(form_frame, bg="#dff0ff")
            frame.pack(pady=5)
            tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
            
            if label == "Maintenanced":
                neo_var = tk.StringVar(value="True")
                dropdown = tk.OptionMenu(frame, neo_var, "True", "False")
                dropdown.config(width=23)
                dropdown.pack(side='left')
                entries.append(neo_var)
                
            else:
                entry = tk.Entry(frame, width=30)
                entry.pack(side='left')
                entries.append(entry)

        def submit():
            airline_id, tail_num, capacity, speed, location_id, maintenanced, model = [e.get() for e in entries]
            
            location_id = location_id if location_id.strip() != "" else None
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("add_airplane", (airline_id, tail_num, int(capacity), int(speed), location_id, "Boeing", bool(maintenanced), model, None))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Boeing airplane added successfully.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add Boeing airplane:\n{e}")
                
            finally:
                conn.close()
    
    # Airbus button
    if plane_type == "airbus":
        tk.Label(form_frame, text="Add Airbus Airplane", font=("Helvetica", 20, "bold"), bg="#dff0ff").pack(pady=20)

        labels = ["Airline ID", "Tail Number", "Seat Capacity", "Speed", "Location ID", "Neo"]
        entries = []

        for label in labels:
            
            frame = tk.Frame(form_frame, bg="#dff0ff")
            frame.pack(pady=5)
            tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
            
            if label == "Neo":
                neo_var = tk.StringVar(value="True")
                dropdown = tk.OptionMenu(frame, neo_var, "True", "False")
                dropdown.config(width=23)
                dropdown.pack(side='left')
                entries.append(neo_var)
            else:
                entry = tk.Entry(frame, width=30)
                entry.pack(side='left')
                entries.append(entry)

        def submit():
            airline_id, tail_num, capacity, speed, location_id, neo = [e.get() for e in entries]
            
            location_id = location_id if location_id.strip() != "" else None
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("add_airplane", (airline_id, tail_num, int(capacity), int(speed), location_id, "Airbus", None, None, bool(neo)))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Airbus airplane added successfully.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add Airbus airplane:\n{e}")
                
            finally:
                conn.close()
    
    # General button
    if plane_type == "general":
        tk.Label(form_frame, text="Add General Airplane", font=("Helvetica", 20, "bold"), bg="#dff0ff").pack(pady=20)

        labels = ["Airline ID", "Tail Number", "Seat Capacity", "Speed", "Location ID"]
        entries = []

        for label in labels:
            
            frame = tk.Frame(form_frame, bg="#dff0ff")
            frame.pack(pady=5)
            tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
            
            if label == "Neo":
                neo_var = tk.StringVar(value="True")
                dropdown = tk.OptionMenu(frame, neo_var, "True", "False")
                dropdown.config(width=23)
                dropdown.pack(side='left')
                entries.append(neo_var)
            else:
                entry = tk.Entry(frame, width=30)
                entry.pack(side='left')
                entries.append(entry)

        def submit():
            airline_id, tail_num, capacity, speed, location_id, neo = [e.get() for e in entries]
            
            location_id = location_id if location_id.strip() != "" else None
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("add_airplane", (airline_id, tail_num, int(capacity), int(speed), location_id, None, None, None, None))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "General airplane added successfully.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add General airplane:\n{e}")
                
            finally:
                conn.close()

    tk.Button(form_frame, text="Submit", command=submit).pack(pady=10)

    tk.Button(
        form_frame,
        text="Back",
        command=lambda: [form_frame.pack_forget(), add_airplane_page()]
    ).pack(pady=10)
    
def add_airport_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    airport_frame = tk.Frame(root, bg="#e6ffe6")
    airport_frame.pack(expand=True, fill="both")
    
    tk.Label(
        airport_frame,
        text="Add Airport",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)


    labels = ["Airport ID", "Airport Name", "City", "State", "Country", "Location ID"]
    entries = []

    for label in labels:
        frame = tk.Frame(airport_frame, bg="#e6ffe6")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#e6ffe6").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)

    def submit():
        airport_id, airport_name, city, state, country, location_id = [e.get() for e in entries]
        
        location_id = location_id if location_id.strip() != "" else None
            
        try:
            conn = connect()
                
            with conn.cursor() as cursor:
                cursor.callproc("add_airport", (airport_id, airport_name, city, state, location_id))
                    
            conn.commit()
                
            messagebox.showinfo("Success", "Airport added successfully.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add airport:\n{e}")
                
        finally:
            conn.close()
    
    tk.Button(airport_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        airport_frame,
        text="Back",
        command=lambda: [airport_frame.pack_forget(), dashboard_frame.pack(expand=True, fill="both")]
    ).pack(pady=10)

def add_person_page():
    global dashboard_frame
    global person_frame
    dashboard_frame.pack_forget()
    
    person_frame = tk.Frame(root, bg="#e6ffe6")
    person_frame.pack(expand=True, fill="both")
    
    tk.Label(
        person_frame,
        text="Select Person Type",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    # Passenger button
    tk.Button(
        person_frame,
        text="Add Passenger",
        width=30,
        command=lambda: [person_frame.pack_forget(), add_person_form(person_frame, "passenger")]
    ).pack(pady=10)
    
    # Pilot button
    tk.Button(
        person_frame,
        text="Add Pilot",
        width=30,
        command=lambda: [person_frame.pack_forget(), add_person_form(person_frame, "pilot")]
    ).pack(pady=10)
    
    tk.Button(
        person_frame,
        text="Back",
        width=20,
        command=lambda: [person_frame.pack_forget(), dashboard_frame.pack(expand=True, fill="both")]
    ).pack(pady=20)

## TODO: ADD PERSON TO PILOT OR PASSENGER
# labels = ["Person ID", "First Name", "Last Name", "Location ID", "Tax ID", "Experience", "Miles", "Funds"]
def add_person_form(prev_frame, person_type):
    global person_form_frame
    person_form_frame = tk.Frame(root, bg="#dff0ff")
    person_form_frame.pack(expand=True, fill="both")
    
    if person_type == "passenger":
        tk.Label(form_frame, text="Add Passenger", font=("Helvetica", 20, "bold"), bg="#dff0ff").pack(pady=20)

        labels = ["Person ID", "First Name", "Last Name", "Location ID", "Miles", "Funds"]
        entries = []

        for label in labels:
            
            frame = tk.Frame(form_frame, bg="#dff0ff")
            frame.pack(pady=5)
            tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
            entry = tk.Entry(frame, width=30)
            entry.pack(side='left')
            entries.append(entry)

        def submit():
            person_id, fname, lname, location_id, miles, funds,  = [e.get() for e in entries]
            
            lname = lname if lname.strip() != "" else None
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("add_person", (person_id, fname, lname, location_id, None, None, int(miles), int(funds)))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Passenger added successfully.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add passenger:\n{e}")
                
            finally:
                conn.close()
    
def clean_exit():
    root.quit()
    root.destroy()

# Welcome buttons
button_frame = tk.Frame(welcome_frame, bg="#f0f0f0")
button_frame.pack(pady=30)

tk.Button(button_frame, text="Procedures Dashboard", width=20, command=go_to_dashboard).grid(row=0, column=0, padx=10, pady=10)
tk.Button(button_frame, text="Views Dashboard", width=20, command=go_to_dashboard).grid(row=0, column=1, padx=10, pady=10)
tk.Button(button_frame, text="Connections Test", width=20, command=test_connection).grid(row=0, column=2, padx=10, pady=10)
tk.Button(button_frame, text="Exit", width=20, command=clean_exit).grid(row=0, column=3, padx=10, pady=10)

# Create window

root.mainloop()