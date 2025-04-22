import tkinter as tk
import tkinter.font as tkFont
from datetime import *
from tkinter import messagebox, ttk

import pymysql

# GUI setup

root = tk.Tk()
root.title("Flight Tracker Database")
root.geometry("1920x1080")
root.configure(bg="#f0f0f0")

# Welcome frame
welcome_frame = tk.Frame(root, bg="#f0f0f0")
welcome_frame.pack(expand=True, fill="both")

## Additional frames
# Create new frames when traveling between page -> form
dashboard_frame = None
form_frame = None
category_frame = None

person_frame = None
person_form_frame = None

views_frame = None

# Info
host = "localhost"
port = 3306
user = "root"
password = None
database = 'flight_tracking'

# CHECK HERE
def connect():
    return pymysql.connect (
            host = host,
            port = port,
            user = user,
            password = password, #insert your password here! Make sure to remove password when committing
            database = database
        )

def test_connection():
    try:
        connection = connect()
        connection.close()
    
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect:\n{e}")

# Procedures dashboard setup
def go_to_dashboard():
    global dashboard_frame
    # Reset frame
    welcome_frame.pack_forget()
    
    dashboard_frame = tk.Frame(root, bg="#e6f2ff")
    dashboard_frame.pack(expand=True, fill="both")
    
    dashboard_frame.columnconfigure(0, weight=1)
    dashboard_frame.rowconfigure(1, weight=1)
    
    button_frame = tk.Frame(dashboard_frame, bg="#e6f2ff")
    button_frame.grid(row=1, column=0)

    # Labels
    tk.Label(
        dashboard_frame,
        text="Procedures Dashboard",
        font=("Helvetica", 20, "bold"),
        bg="#e6f2ff"
    ).grid(row=0, column=0, pady=20)
    
    tk.Label(button_frame, text="Add / Remove", font=("Helvetica", 14, "bold"), bg="#e6f2ff").grid(row=0, column=0, pady=(0, 10))
    tk.Label(button_frame, text="Flight Operations", font=("Helvetica", 14, "bold"), bg="#e6f2ff").grid(row=0, column=1, pady=(0, 10))
    tk.Label(button_frame, text="People Operations", font=("Helvetica", 14, "bold"), bg="#e6f2ff").grid(row=0, column=2, pady=(0, 10))

    # Buttons
    
    add_and_license = {
        "Add Airplane": add_airplane_page,
        "Add Airport": add_airport_page,
        "Add Person": add_person_page,
        "Grant/Revoke License": pilot_license_page
    }
    
    flight_ops = {
        "Offer Flight": offer_flight_page,
        "Flight Landing": flight_landing_page,
        "Flight Takeoff": flight_takeoff_page,
        "Retire Flight": retire_flight_page
    }
    
    other_procedures = {
        "Assign Pilot": assign_pilot_page,
        "Passengers Board": passengers_board_page,
        "Passengers Disembark": passengers_disembark_page,
        "Recycle Crew": recycle_crew_page
    }
    
    def populate_column(procs, col):
        for idx, (label, func) in enumerate(procs.items()):
            tk.Button(
                button_frame,
                text=label,
                width=25,
                command=func
            ).grid(row=idx + 1, column=col, padx=10, pady=5)
            
    populate_column(add_and_license, 0)
    populate_column(flight_ops, 1)
    populate_column(other_procedures, 2)
    
    # procedures = {
    #     "add_airplane" : add_airplane_page,
    #     "add_airport" : add_airport_page,
    #     "add_person" : add_person_page,
    #     "grant_or_revoke_pilot_license" : pilot_license_page,
    #     "offer_flight" : offer_flight_page,
    #     "flight_landing" : flight_landing_page,
    #     "flight_takeoff" : flight_takeoff_page,
    #     "passengers_board" : passengers_board_page,
    #     "passengers_disembark" : passengers_disembark_page,
    #     "assign_pilot" : assign_pilot_page,
    #     "recycle_crew" : recycle_crew_page,
    #     "retire_flight" : retire_flight_page,
    # }
    
    
    # for idx, (proc, func) in enumerate(procedures.items()):
    #     tk.Button(
    #         button_frame,
    #         text=proc.replace("_", " ").title(),
    #         width=30,
    #         command=func
    #     ).grid(row=idx // 2, column=idx % 2, padx=10, pady=5)
    
    nav_frame = tk.Frame(dashboard_frame, bg="#e6f2ff")
    nav_frame.grid(row=2, column=0, pady=20)
    
    tk.Button(
        nav_frame,
        text="Back",
        width=20,
        command=lambda: [dashboard_frame.pack_forget(), welcome_frame.pack(expand=True, fill="both")]
    ).grid(row=0, column=0, padx=10)
    
    
    tk.Button(
        nav_frame,
        text="Simulate Cycle",
        width=20,
        command=simulation
    ).grid(row=0, column=1, padx=10)

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

# add_airport() setup
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
                cursor.callproc("add_airport", (airport_id, airport_name, city, state, country, location_id))
                
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

# add_person setup
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

def add_person_form(prev_frame, person_type):
    global person_form_frame
    person_form_frame = tk.Frame(root, bg="#dff0ff")
    person_form_frame.pack(expand=True, fill="both")
    
    if person_type == "passenger":
        tk.Label(person_form_frame, text="Add Passenger", font=("Helvetica", 20, "bold"), bg="#dff0ff").pack(pady=20)

        labels = ["Passenger ID", "First Name", "Last Name", "Location ID", "Miles", "Funds"]
        entries = []

        for label in labels:
            
            frame = tk.Frame(person_form_frame, bg="#dff0ff")
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
        
        tk.Button(
            person_form_frame,
            text="Back",
            command=lambda: [person_form_frame.pack_forget(), add_person_page()]
        ).pack(pady=10)
            
    
    if person_type == "pilot":
        tk.Label(person_form_frame, text="Add Pilot", font=("Helvetica", 20, "bold"), bg="#dff0ff").pack(pady=20)

        labels = ["Pilot ID", "First Name", "Last Name", "Location ID", "Tax ID", "Experience"]
        entries = []

        for label in labels:
            
            frame = tk.Frame(person_form_frame, bg="#dff0ff")
            frame.pack(pady=5)
            tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
            entry = tk.Entry(frame, width=30)
            entry.pack(side='left')
            entries.append(entry)

        def submit():
            person_id, fname, lname, location_id, tax_id, experience = [e.get() for e in entries]
            
            lname = lname if lname.strip() != "" else None
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("add_person", (person_id, fname, lname, location_id, tax_id, int(experience), None, None))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Pilot added successfully.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add pilot:\n{e}")
                
            finally:
                conn.close()
        
        tk.Button(person_form_frame, text="Submit", command=submit).pack(pady=10)
        
        tk.Button(
            person_form_frame,
            text="Back",
            command=lambda: [person_form_frame.pack_forget(), add_person_page()]
        ).pack(pady=10)
    
# grant_or_revoke_pilot_license() setup
def pilot_license_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    pilot_license_frame = tk.Frame(root, bg="#e6ffe6")
    pilot_license_frame.pack(expand=True, fill="both")
    
    tk.Label(
        pilot_license_frame,
        text="Grant or Remove License From Pilot",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    tk.Label(
        pilot_license_frame,
        text="Type in pilot license to add or remove.",
        font=("Helvetica", 16),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Pilot ID", "License Name"]
    entries = []

    for label in labels:
        
        frame = tk.Frame(pilot_license_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
        
    def submit():
            person_id, license = [e.get() for e in entries]
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("grant_or_revoke_pilot_license", (person_id, license))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "License change completed.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to perform license change:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(pilot_license_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        pilot_license_frame,
        text="Back",
        command=lambda: [pilot_license_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)
    
# offer_flight() setup
def offer_flight_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    offer_flight_frame = tk.Frame(root, bg="#e6ffe6")
    offer_flight_frame.pack(expand=True, fill="both")
    
    tk.Label(
        offer_flight_frame,
        text="Offer Flight",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Flight ID", "Route ID", "Supporting Airline", "Supporting Tail", "Progress", "Next Time", "Cost"]
    entries = []

    for label in labels:
        
        frame = tk.Frame(offer_flight_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
        
        if (label == "Next Time"):
            entry.insert(0, "HH:MM:SS")
            entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end'))
        
    def submit():
            flight_id, route_id, support_airline, support_tail, progress, next_time, cost = [e.get() for e in entries]
            
            next_time = datetime.strptime(next_time, "%H:%M:%S").time()
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("offer_flight", (flight_id, route_id, support_airline, support_tail, int(progress), next_time, int(cost)))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Flight offered.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to offer flight:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(offer_flight_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        offer_flight_frame,
        text="Back",
        command=lambda: [offer_flight_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)

# flight_landing() setup
def flight_landing_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    flight_frame = tk.Frame(root, bg="#e6ffe6")
    flight_frame.pack(expand=True, fill="both")
    
    tk.Label(
        flight_frame,
        text="Flight Landing",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Flight ID"]
    entries = []
    
    for label in labels:
        
        frame = tk.Frame(flight_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
        
    def submit():
            flight_id = [e.get() for e in entries]
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("flight_landing", (flight_id))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Flight landed.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to land flight:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(flight_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        flight_frame,
        text="Back",
        command=lambda: [flight_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)

# flight takeoff() setup
def flight_takeoff_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    flight_frame = tk.Frame(root, bg="#e6ffe6")
    flight_frame.pack(expand=True, fill="both")
    
    tk.Label(
        flight_frame,
        text="Flight Takeoff",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Flight ID"]
    entries = []
    
    for label in labels:
        
        frame = tk.Frame(flight_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
        
    def submit():
            flight_id = [e.get() for e in entries]
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("flight_takeoff", (flight_id))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Flight taken off.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to take off flight:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(flight_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        flight_frame,
        text="Back",
        command=lambda: [flight_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)

# passengers_board() setup
def passengers_board_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    flight_frame = tk.Frame(root, bg="#e6ffe6")
    flight_frame.pack(expand=True, fill="both")
    
    tk.Label(
        flight_frame,
        text="Passenger Boarding",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Flight ID"]
    entries = []
    
    for label in labels:
        
        frame = tk.Frame(flight_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
        
    def submit():
            flight_id = [e.get() for e in entries]
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("passengers_board", (flight_id))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Passengers boarded.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to board passengers:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(flight_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        flight_frame,
        text="Back",
        command=lambda: [flight_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)
    
# passengers_disembark() setup
def passengers_disembark_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    flight_frame = tk.Frame(root, bg="#e6ffe6")
    flight_frame.pack(expand=True, fill="both")
    
    tk.Label(
        flight_frame,
        text="Passenger Disembark",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Flight ID"]
    entries = []
    
    for label in labels:
        
        frame = tk.Frame(flight_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
        
    def submit():
            flight_id = [e.get() for e in entries]
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("passengers_disembark", (flight_id))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Passengers disembarked.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to disembark passengers:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(flight_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        flight_frame,
        text="Back",
        command=lambda: [flight_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)

# assign_pilot() setup
def assign_pilot_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    assign_pilot_frame = tk.Frame(root, bg="#e6ffe6")
    assign_pilot_frame.pack(expand=True, fill="both")
    
    tk.Label(
        assign_pilot_frame,
        text="Assign Pilot to Flight",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Flight ID", "Pilot ID"]
    entries = []
    
    for label in labels:
        
        frame = tk.Frame(assign_pilot_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
    
    def submit():
            flight_id, pilot_id = [e.get() for e in entries]
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("assign_pilot", (flight_id, pilot_id))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Pilot assigned.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to assign pilot:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(assign_pilot_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        assign_pilot_frame,
        text="Back",
        command=lambda: [assign_pilot_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)

# recycle_crew() setup
def recycle_crew_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    flight_frame = tk.Frame(root, bg="#e6ffe6")
    flight_frame.pack(expand=True, fill="both")
    
    tk.Label(
        flight_frame,
        text="Recycling Crew",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Flight ID"]
    entries = []
    
    for label in labels:
        
        frame = tk.Frame(flight_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
        
    def submit():
            flight_id = [e.get() for e in entries]
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("recycle_crew", (flight_id))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Crew recycled.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to recycle crew:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(flight_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        flight_frame,
        text="Back",
        command=lambda: [flight_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)

# retire_flight() setup
def retire_flight_page():
    global dashboard_frame
    dashboard_frame.pack_forget()
    
    flight_frame = tk.Frame(root, bg="#e6ffe6")
    flight_frame.pack(expand=True, fill="both")
    
    tk.Label(
        flight_frame,
        text="Retiring Flight",
        font=("Helvetica", 20, "bold"),
        bg="#e6ffe6"
    ).pack(pady=30)
    
    labels = ["Flight ID"]
    entries = []
    
    for label in labels:
        
        frame = tk.Frame(flight_frame, bg="#dff0ff")
        frame.pack(pady=5)
        tk.Label(frame, text=label + ":", width=15, anchor='w', bg="#dff0ff").pack(side='left')
        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)
        
    def submit():
            flight_id = [e.get() for e in entries]
            
            try:
                conn = connect()
                
                with conn.cursor() as cursor:
                    cursor.callproc("retire_flight", (flight_id))
                    
                conn.commit()
                
                messagebox.showinfo("Success", "Flight retired.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to retire flight:\n{e}")
                
            finally:
                conn.close()
        
    tk.Button(flight_frame, text="Submit", command=submit).pack(pady=10)
    
    tk.Button(
        flight_frame,
        text="Back",
        command=lambda: [flight_frame.pack_forget(), go_to_dashboard()]
    ).pack(pady=10)

# simulation_cycle() setup
def simulation():
    try:
        conn = connect()
                
        with conn.cursor() as cursor:
            cursor.callproc("simulate_cycle")
                    
            conn.commit()
                
            messagebox.showinfo("Success", "Flights simulated.")
                
    except Exception as e:
        messagebox.showerror("Error", f"Failed to simulate database:\n{e}")
                
    finally:
        conn.close()

# Views dashboard setup
def go_to_views():
    global views_frame
    welcome_frame.pack_forget()
    
    views_frame = tk.Frame(root, bg="#e6f2ff")
    views_frame.pack(expand=True, fill="both")
    
    tk.Label(
        views_frame,
        text="Views Dashboard",
        font=("Helvetica", 20, "bold"),
        bg="#e6f2ff"
    ).pack(pady=20)
    
    button_frame = tk.Frame(views_frame, bg="#e6f2ff")
    button_frame.pack(pady=10)
    
    views = {"Flights in the Air" : "flights_in_the_air", 
            "Flights on the Ground" : "flights_on_the_ground", 
            "People in the Air" : "people_in_the_air", 
            "People on the Ground" : "people_on_the_ground", 
            "Route Summary" : "route_summary", 
            "Alternative Flights" : "alternative_airports"}
    
    for idx, (label, view_name) in enumerate(views.items()):
        tk.Button(
            button_frame,
            text=label,
            width=30,
            command=lambda vn=view_name: show_view(label, vn)
        ).grid(row=idx, column=0, pady=5)
    
    tk.Button(
        views_frame,
        text="Back",
        command=lambda: [views_frame.pack_forget(), welcome_frame.pack(expand=True, fill="both")]
    ).pack(pady=20)

def show_view(label_name, view_name):
    global views_frame
    views_frame.pack_forget()
    
    precursor_frame = tk.Frame(root, bg="#ffffff")
    precursor_frame.pack(pady=10)
    
    font = tkFont.Font()
    
    tk.Label(
        precursor_frame,
        text=label_name,
        font=("Helvetica", 20, "bold"),
        bg="#000000"
    ).pack(pady=30)
    
    data_frame = tk.Frame(precursor_frame, bg="#ffffff")
    data_frame.pack(pady=10)
    
    try:
        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {view_name}")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
    
    except Exception as e:
        messagebox.showerror("Error", f" Could load view '{view_name}':\n{e}")
        return
    
    finally:
        conn.close()
        
    for x in data_frame.winfo_children():
        x.destroy()
    
    tree = ttk.Treeview(data_frame, columns=columns, show="headings")
    
    for col in columns:
        max_width = font.measure(col) + 70
        
        for row in rows:
            cell_text = str(row[columns.index(col)])
            cell_width = font.measure(cell_text)
            
            if cell_width > max_width:
                max_width = cell_width
        
        tree.heading(col, text=col)
        tree.column(col, width=max_width, anchor="w")
        
    for row in rows:
        tree.insert("", "end", values=row)


    tree.pack(side="left", fill="both", expand=True)

    v_scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
    v_scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=v_scrollbar.set)
    
    h_scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=tree.xview)
    h_scrollbar.pack(fill="x")
    tree.configure(xscrollcommand=h_scrollbar.set)
    
    tk.Button(
        precursor_frame,
        text="Back",
        command=lambda: [precursor_frame.pack_forget(), data_frame.pack_forget(), views_frame.pack(expand=True, fill="both")]
    ).pack(pady=10)

def clean_exit():
    root.quit()
    root.destroy()
    
# start page setup
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

# Welcome buttons
button_frame = tk.Frame(welcome_frame, bg="#f0f0f0")
button_frame.pack(pady=30)

tk.Button(button_frame, text="Procedures Dashboard", width=20, command=go_to_dashboard).grid(row=0, column=0, padx=10, pady=10)
tk.Button(button_frame, text="Views Dashboard", width=20, command=go_to_views).grid(row=0, column=1, padx=10, pady=10)
tk.Button(button_frame, text="Connections Test", width=20, command=test_connection).grid(row=0, column=2, padx=10, pady=10)
tk.Button(button_frame, text="Exit", width=20, command=clean_exit).grid(row=0, column=3, padx=10, pady=10)

# Create window
root.mainloop()