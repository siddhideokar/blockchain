import streamlit as st
import hashlib
import json

# Initialize an empty hospital ledger (using session state for persistence)
if 'hospital_ledger' not in st.session_state:
    st.session_state.hospital_ledger = {}

# Function to generate a unique hash for data integrity
def generate_hash(patient_name, treatment, cost, date_of_visit):
    hash_input = f"{patient_name}{treatment}{cost}{date_of_visit}"
    return hashlib.md5(hash_input.encode()).hexdigest()

# Streamlit UI
st.title("🏥 Hospital Ledger Management")

# Section to add a patient visit
st.header("Add or Update Patient Visit")

patient_name = st.text_input("Enter patient's name").strip().lower()
treatment = st.text_input("Enter treatment received")
cost = st.number_input("Enter treatment cost ($)", min_value=0.0, format="%.2f")
date_of_visit = st.date_input("Enter date of visit").strftime("%Y-%m-%d")

if st.button("Add/Update Visit"):
    if patient_name and treatment and cost:
        visit_hash = generate_hash(patient_name, treatment, cost, date_of_visit)
        visit = {
            "treatment": treatment,
            "cost": cost,
            "date_of_visit": date_of_visit,
            "visit_hash": visit_hash
        }

        # Add or update patient record
        if patient_name not in st.session_state.hospital_ledger:
            st.session_state.hospital_ledger[patient_name] = []

        st.session_state.hospital_ledger[patient_name].append(visit)
        st.success(f"Visit recorded for {patient_name} on {date_of_visit}. Hash: {visit_hash}")
    else:
        st.error("Please fill in all fields correctly.")

# Section to search for a patient visit
st.header("🔍 Search for Patient Visits")
search_patient = st.text_input("Enter patient name to search").strip().lower()

if st.button("Search"):
    if search_patient in st.session_state.hospital_ledger:
        st.subheader(f"Visit Records for {search_patient.capitalize()}")
        for visit in st.session_state.hospital_ledger[search_patient]:
            st.json(visit, expanded=False)
    else:
        st.warning(f"Patient {search_patient} not found in the ledger.")

# Show all stored data
st.header("📋 Hospital Ledger Data")
if st.checkbox("Show All Data"):
    st.json(st.session_state.hospital_ledger, expanded=False)
