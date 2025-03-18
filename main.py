from tkinter import *
import tkinter as tk
from tkinter import messagebox, scrolledtext
import uuid
import csv
import os
import time
from threading import Thread
import pywhatkit as kit

# csv file setup where data stored
CSV_FILE = "data.csv"

# Predefined symptom-disease-medicine mapping
SYMPTOM_DISEASE_MEDICINE = {
    "fever": {"disease": "Common Cold", "medicine": "Paracetamol"},
    "cough": {"disease": "Common Cold", "medicine": "Cough Syrup"},
    "headache": {"disease": "Migraine", "medicine": "Ibuprofen"},
    "sore throat": {"disease": "Strep Throat", "medicine": "Amoxicillin"},
    "rash": {"disease": "Allergy", "medicine": "Antihistamine"},
    "nausea": {"disease": "Food Poisoning", "medicine": "Domperidone"},
    "vomiting": {"disease": "Food Poisoning", "medicine": "Ondansetron"},
    "diarrhea": {"disease": "Gastroenteritis", "medicine": "Loperamide"},
    "chest pain": {"disease": "Angina", "medicine": "Nitroglycerin"},
    "shortness of breath": {"disease": "Asthma", "medicine": "Salbutamol"},
    "fatigue": {"disease": "Anemia", "medicine": "Iron Supplements"},
    "joint pain": {"disease": "Arthritis", "medicine": "Naproxen"},
    "back pain": {"disease": "Muscle Strain", "medicine": "Diclofenac"},
    "abdominal pain": {"disease": "Gastritis", "medicine": "Omeprazole"},
    "dizziness": {"disease": "Vertigo", "medicine": "Meclizine"},
    "blurred vision": {"disease": "Diabetes", "medicine": "Insulin"},
    "frequent urination": {"disease": "Urinary Tract Infection", "medicine": "Ciprofloxacin"},
    "swelling": {"disease": "Edema", "medicine": "Furosemide"},
    "constipation": {"disease": "Irritable Bowel Syndrome", "medicine": "Psyllium Husk"},
    "heartburn": {"disease": "Acid Reflux", "medicine": "Ranitidine"},
    "insomnia": {"disease": "Sleep Disorder", "medicine": "Melatonin"},
    "weight loss": {"disease": "Hyperthyroidism", "medicine": "Methimazole"},
    "weight gain": {"disease": "Hypothyroidism", "medicine": "Levothyroxine"},
    "itchy skin": {"disease": "Eczema", "medicine": "Hydrocortisone Cream"},
    "red eyes": {"disease": "Conjunctivitis", "medicine": "Antibiotic Eye Drops"},
    "ear pain": {"disease": "Ear Infection", "medicine": "Amoxicillin"},
    "toothache": {"disease": "Dental Caries", "medicine": "Ibuprofen"},
    "muscle cramps": {"disease": "Electrolyte Imbalance", "medicine": "Potassium Supplements"},
    "cold hands and feet": {"disease": "Raynaud's Disease", "medicine": "Nifedipine"},
    "high blood pressure": {"disease": "Hypertension", "medicine": "Amlodipine"},
    "low blood pressure": {"disease": "Hypotension", "medicine": "Fludrocortisone"},
    "palpitations": {"disease": "Arrhythmia", "medicine": "Metoprolol"},
    "memory loss": {"disease": "Alzheimer's Disease", "medicine": "Donepezil"},
    "tremors": {"disease": "Parkinson's Disease", "medicine": "Levodopa"},
    "seizures": {"disease": "Epilepsy", "medicine": "Phenytoin"},
    "difficulty swallowing": {"disease": "Esophagitis", "medicine": "Pantoprazole"},
    "blood in stool": {"disease": "Hemorrhoids", "medicine": "Witch Hazel"},
    "blood in urine": {"disease": "Kidney Stones", "medicine": "Tamsulosin"},
    "excessive thirst": {"disease": "Diabetes", "medicine": "Metformin"},
    "excessive hunger": {"disease": "Hyperthyroidism", "medicine": "Methimazole"},
    "night sweats": {"disease": "Tuberculosis", "medicine": "Isoniazid"},
    "hair loss": {"disease": "Alopecia", "medicine": "Minoxidil"},
    "bruising easily": {"disease": "Vitamin Deficiency", "medicine": "Vitamin C"},
    "stiff neck": {"disease": "Meningitis", "medicine": "Ceftriaxone"},
    "confusion": {"disease": "Dehydration", "medicine": "Oral Rehydration Solution"},
    "loss of appetite": {"disease": "Depression", "medicine": "Fluoxetine"},
    "swollen lymph nodes": {"disease": "Infection", "medicine": "Antibiotics"},
    "dry mouth": {"disease": "Sjogren's Syndrome", "medicine": "Pilocarpine"},
    "dry eyes": {"disease": "Sjogren's Syndrome", "medicine": "Artificial Tears"},
    "cracked lips": {"disease": "Vitamin Deficiency", "medicine": "Vitamin B Complex"},
    "nosebleeds": {"disease": "Dry Air", "medicine": "Saline Nasal Spray"},
    "wheezing": {"disease": "Asthma", "medicine": "Montelukast"},
    "snoring": {"disease": "Sleep Apnea", "medicine": "CPAP Machine"},
    "hoarseness": {"disease": "Laryngitis", "medicine": "Voice Rest"},
    "frequent infections": {"disease": "Immunodeficiency", "medicine": "Immunoglobulin Therapy"},
}

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Health ID", "Contact", "Name", "Date", "Disease", "Medicine", "Interval (mins)", "User Choice Medicine"])

def find_user_by_id(health_id):
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == health_id:
                return row  #return data already exist for patient
    return None

def save_info():
    health_id = id_entry.get().strip()
    contact = contact_entry.get().strip()
    name = name_entry.get().strip()
    date = date_entry.get().strip()
    disease = disease_entry.get().strip()
    medicine = medicine_entry.get().strip()
    interval = interval_entry.get().strip()
    user_choice_medicine = user_choice_entry.get().strip()
    
    if not contact or not name or not date or not disease or not medicine or not interval:
        messagebox.showerror("Error", "Fill all fields!")
        return
    
    if not health_id:
        health_id = str(uuid.uuid4())[:8]
    
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([health_id, contact, name, date, disease, medicine, interval, user_choice_medicine])
    messagebox.showinfo("Success", f"Data saved with Health ID: {health_id}")
    
    if interval.isdigit():
        reminder_thread = Thread(target=medicine_reminder, args=(contact, medicine, int(interval)))
        reminder_thread.daemon = True
        reminder_thread.start()
    
    #clear all details once fetched
    id_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    date_entry.delete(0,tk.END)
    disease_entry.delete(0, tk.END)
    medicine_entry.delete(0, tk.END)
    interval_entry.delete(0, tk.END)
    user_choice_entry.delete(0, tk.END)

def medicine_reminder(contact, medicine, interval):
    while True:
        time.sleep(interval * 60)
        message = f"Reminder: It's time to take your medicine - {medicine}. Stay Healthy!"
        print(f"Sending WhatsApp message to {contact}: {message}")
        kit.sendwhatmsg_instantly(f"+91{contact}", message, wait_time=10, tab_close=True)

# view all records
def display_info():
    info_window = tk.Toplevel(root)
    info_window.title("User Data")
    info_window.geometry("500x400")
    
    scroll_text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, width=60, height=20)
    scroll_text.pack(padx=10, pady=10)

    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header there only heading i wrote of entry items
        records_found = False
        for row in reader:
            records_found = True
            scroll_text.insert(tk.END, f"Health ID: {row[0]}\n")
            scroll_text.insert(tk.END, f"Contact: {row[1]}\n")
            scroll_text.insert(tk.END, f"Name: {row[2]}\n")
            scroll_text.insert(tk.END, f"Date: {row[3]}\n")
            scroll_text.insert(tk.END, f"Disease: {row[4]}\n")
            scroll_text.insert(tk.END, f"Medicine: {row[5]}\n")
            scroll_text.insert(tk.END, f"Interval: {row[6]} minutes\n")
            scroll_text.insert(tk.END, f"User Choice Medicine: {row[7]}\n")
            scroll_text.insert(tk.END, "-" * 20 + "\n")
        
        if not records_found:
            scroll_text.insert(tk.END, " Norecords found")
    
    # Disable editing in the scrolled text widget ---> not editable window
    scroll_text.configure(state="disabled")
    
    # Add a close button
    tk.Button(info_window, text="Close", command=info_window.destroy).pack(pady=10)



def check_history():
    health_id = history_entry.get().strip()
    if not health_id:
        messagebox.showerror("Error", "Please enter a Health ID!")
        return
    
    # Open new tab to display info of particular health id
    history_window = tk.Toplevel(root)
    history_window.title(f"Health History for ID: {health_id}")
    history_window.geometry("500x400")
    
    scroll_text = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, width=60, height=20)
    scroll_text.pack(padx=10, pady=10)
    
    # Read the CSV file and find all records for the given Health ID
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header there only heading i wrote of entry items
        records_found = False
        for row in reader:    # History of start to end of particular health id
            if row[0] == health_id:
                records_found = True
                scroll_text.insert(tk.END, f"Health ID: {row[0]}\n")
                scroll_text.insert(tk.END, f"Contact: {row[1]}\n")
                scroll_text.insert(tk.END, f"Name: {row[2]}\n")
                scroll_text.insert(tk.END, f"Date: {row[3]}\n")
                scroll_text.insert(tk.END, f"Disease: {row[4]}\n")
                scroll_text.insert(tk.END, f"Medicine: {row[5]}\n")
                scroll_text.insert(tk.END, f"Interval: {row[6]} minutes\n")
                scroll_text.insert(tk.END, f"User Choice Medicine: {row[7]}\n")
                scroll_text.insert(tk.END, "-" * 50 + "\n")
        
        if not records_found:
            scroll_text.insert(tk.END, " Norecords found for the given Health ID.")
    
    # Disable editing in the scrolled text widget ---> not editable window
    scroll_text.configure(state="disabled")
    
    # Add a close button
    tk.Button(history_window, text="Close", command=history_window.destroy).pack(pady=10)

def suggest_medicine():
    symptom = symptom_entry.get().strip().lower()
    if symptom in SYMPTOM_DISEASE_MEDICINE:
        disease = SYMPTOM_DISEASE_MEDICINE[symptom]["disease"]
        medicine = SYMPTOM_DISEASE_MEDICINE[symptom]["medicine"]
        disease_entry.delete(0, tk.END)
        disease_entry.insert(0, disease)
        medicine_entry.delete(0, tk.END)
        medicine_entry.insert(0, medicine)
    else:
        messagebox.showinfo("Info", "No suggestion available for the given symptom.")

initialize_csv()

root = tk.Tk()
root.title("Health ID Manager")
root.geometry("400x1000")

tk.Label(root, text="Health ID Registration", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Health ID (Leave empty if new):").pack(anchor="w", padx=20)
id_entry = tk.Entry(root, width=30)
id_entry.pack(padx=20, pady=5)

tk.Label(root, text="Contact:").pack(anchor="w", padx=20)
contact_entry = tk.Entry(root, width=30)
contact_entry.pack(padx=20, pady=5)

tk.Label(root, text="Name:").pack(anchor="w", padx=20)
name_entry = tk.Entry(root, width=30)
name_entry.pack(padx=20, pady=5)

tk.Label(root, text="Date:").pack(anchor="w", padx=20)
date_entry = tk.Entry(root, width=30)
date_entry.pack(padx=20, pady=5)

tk.Label(root, text="Symptom:").pack(anchor="w", padx=20)
symptom_entry = tk.Entry(root, width=30)
symptom_entry.pack(padx=20, pady=5)

tk.Button(root, text="Suggest Medicine", command=suggest_medicine).pack(pady=5)

tk.Label(root, text="Disease:").pack(anchor="w", padx=20)
disease_entry = tk.Entry(root, width=30)
disease_entry.pack(padx=20, pady=5)

tk.Label(root, text="Medicine:").pack(anchor="w", padx=20)
medicine_entry = tk.Entry(root, width=30)
medicine_entry.pack(padx=20, pady=5)

tk.Label(root, text="Interval (mins):").pack(anchor="w", padx=20)
interval_entry = tk.Entry(root, width=30)
interval_entry.pack(padx=20, pady=5)

tk.Label(root, text="User Choice Medicine:").pack(anchor="w", padx=20)
user_choice_entry = tk.Entry(root, width=30)
user_choice_entry.pack(padx=20, pady=5)

tk.Button(root, text="Save Information", command=save_info).pack(pady=10)

tk.Label(root, text="Check History by Health ID", font=("Arial", 14, "bold")).pack(pady=15)

tk.Label(root, text="Enter Health ID:").pack(anchor="w", padx=20)
history_entry = tk.Entry(root, width=30)
history_entry.pack(padx=20, pady=5)

tk.Button(root, text="Check History", command=check_history).pack(pady=10)

tk.Button(root, text="View All Records", command=display_info).pack(pady=10)

root.mainloop()
