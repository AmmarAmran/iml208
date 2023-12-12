import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.title('Subject Registration')
root.geometry('1024x1024')
root.configure(bg='#1A1A1A')

#Entry limitations
def validate_input(num):
    if num.isdigit() or num == "" or num == "\b":
        if len(num) <= 10:
            return True
    return False

def validate_input2(letter):
    if all(c.isalpha() or c.isspace() for c in letter) or letter == "" or letter == "\b":
        return True
    return False

validate_cmd = root.register(validate_input)
validate_cmd2 = root.register(validate_input2)

# Data structure to store registrations
registrations = []

# Function to handle the registration submission
def register():
    name = name_entry.get()
    email = email_entry.get()
    matrix = matrix_entry.get()
    selected_subjects = [subject_labels[i] for i in range(len(subject_vars)) if subject_vars[i].get()]

    if not name or not email or not selected_subjects:
        messagebox.showerror("Error", "Please fill in all fields and select at least one subject.")
    else:
        registration = {
            "Name": name,
            "Email": email,
            "Matrix": matrix,
            "Selected Subjects": selected_subjects
        }
        registrations.append(registration)
        update_registration_list()
        clear_fields()
        messagebox.showinfo("Registration Successful", "Thank you for registering!")
        
        df = pd.DataFrame(registrations)
        df.to_excel("registrations.xlsx", index=False)

def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    matrix_entry.delete(0, tk.END)
    for i in range(len(subject_vars)):
        subject_vars[i].set(False)

def update_registration_list():
    registration_list.delete(0, tk.END)
    for i, registration in enumerate(registrations, start=1):
        registration_list.insert(tk.END, f"Registration {i}: Name: {registration['Name']}, Email: {registration['Email']}, Matrix: {registration['Matrix']}, Subjects: {', '.join(registration['Selected Subjects'])}")

def delete_registration():
    selected_index = registration_list.curselection()
    if selected_index:
        index = selected_index[0]
        registrations.pop(index)
        update_registration_list()

def edit_registration():
    selected_index = registration_list.curselection()
    if selected_index:
        index = selected_index[0]
        registration = registrations[index]
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Registration")
        edit_window.geometry('480x480')
        
        # Create and pack widgets in the edit window
        name_label = tk.Label(edit_window, text="Name:", font=("Arial", 16))
        name_label.pack()
        
        name_edit = tk.Entry(edit_window, font=("Arial", 16))
        name_edit.insert(0, registration["Name"])
        name_edit.pack()
        
        matrix_label = tk.Label(edit_window, text="Matrix Number:", font=("Arial", 16))
        matrix_label.pack()
        
        matrix_edit = tk.Entry(edit_window, font=("Arial", 16))
        matrix_edit.insert(0, registration["Matrix"])
        matrix_edit.pack()
        
        email_label = tk.Label(edit_window, text="Email:", font=("Arial", 16))
        email_label.pack()
        
        email_edit = tk.Entry(edit_window, font=("Arial", 16))
        email_edit.insert(0, registration["Email"])
        email_edit.pack()
        
        subject_edit_vars = [tk.BooleanVar() for _ in range(7)]
        
        for i in range(7):
            subject_check = tk.Checkbutton(edit_window, text=subject_labels[i], variable=subject_edit_vars[i], font=("Arial", 16))
            if subject_labels[i] in registration["Selected Subjects"]:
                subject_check.select()
            subject_check.pack()
        
        def save_changes():
            registration["Name"] = name_edit.get()
            registration["Email"] = email_edit.get()
            registration["Selected Subjects"] = [subject_labels[i] for i in range(7) if subject_edit_vars[i].get()]
            edit_window.destroy()
            update_registration_list()
        
        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes, font=("Arial", 16))
        save_button.pack()
        
def display_registered_data():
    if registrations:
        for i, registration in enumerate(registrations, start=1):
            messagebox.showinfo(f"Registration {i}", f"Name: {registration['Name']}\nEmail: {registration['Email']}\nSubjects: {', '.join(registration['Selected Subjects'])}")
    else:
        messagebox.showinfo("No Registrations", "There are no registered data.")

frame = tk.Frame(bg='#1E1E1E')

# Create and pack widgets
title_label = tk.Label(root, text="Subject Registration:", bg='#1A1A1A', fg='#FF3399', font=('Arial', 30))
title_label.pack()

name_label = tk.Label(root, text="Name:", bg='#1A1A1A', fg='#FF3399', font=('Arial', 16))
name_label.pack()
name_entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd2, "%P"), font=("Arial", 16))
name_entry.pack()

matrix = tk.Label(root, text="Matrix Number:", bg='#1A1A1A', fg='#FF3399', font=('Arial', 16))
matrix.pack()
matrix_entry = tk.Entry(root, validate= 'key', validatecommand=(validate_cmd, "%P"), font=('Arial', 16))
matrix_entry.pack()

email_label = tk.Label(root, text="Email:", bg='#1A1A1A', fg='#FF3399', font=('Arial', 16))
email_label.pack()
email_entry = tk.Entry(root, font=("Arial", 16))
email_entry.pack()

subject_vars = [tk.BooleanVar() for _ in range(7)]  # Create BooleanVars for subjects

subject_labels = ["CTU264", "ELC231", "HBU135", "IML206", "IML207", "IML208", "IML209"]
for i in range(7):
    subject_check = tk.Checkbutton(root, text=subject_labels[i], variable=subject_vars[i], bg='#1A1A1A', fg='#FF3399', font=('Arial', 16))
    subject_check.pack(side= tk.TOP, padx= 1)
    
list_frame = tk.Frame(root, bg='#1A1A1A')
list_frame.pack(side=tk.RIGHT)
registration_list = tk.Listbox(list_frame, selectmode=tk.SINGLE, font=("Arial", 14), bg='#00688B', fg='#FFFFFF', height=40)
registration_list.pack(fill=tk.BOTH, expand=True)

register_button = tk.Button(root, text="Register", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=register)
register_button.pack(side=tk.TOP, pady=1)

edit_button = tk.Button(root, text="Edit", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=edit_registration)
edit_button.pack(side= tk.TOP, pady= 1)

delete_button = tk.Button(root, text="Delete", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=delete_registration)
delete_button.pack(side= tk.TOP, pady = 1)

display_button = tk.Button(root, text="Display Data", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=display_registered_data)
display_button.pack(side= tk.TOP, pady = 1)

update_registration_list()  # Initial display of registrations

frame.pack()

# Start the main loop
root.mainloop()