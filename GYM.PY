import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state to store the ledger
if "ledger" not in st.session_state:
    st.session_state["ledger"] = pd.DataFrame(columns=["Name", "Membership Type", "Join Date", "Payment Amount", "Last Payment Date"])

# Function to add a new member to the ledger
def add_member(name, membership_type, payment_amount):
    new_member = {
        "Name": name,
        "Membership Type": membership_type,
        "Join Date": datetime.now().strftime("%Y-%m-%d"),
        "Payment Amount": payment_amount,
        "Last Payment Date": datetime.now().strftime("%Y-%m-%d"),
    }
    st.session_state["ledger"] = pd.concat([st.session_state["ledger"], pd.DataFrame([new_member])], ignore_index=True)

# Function to log a payment for an existing member
def log_payment(member_name, payment_amount):
    ledger = st.session_state["ledger"]
    if member_name in ledger["Name"].values:
        ledger.loc[ledger["Name"] == member_name, "Payment Amount"] += payment_amount
        ledger.loc[ledger["Name"] == member_name, "Last Payment Date"] = datetime.now().strftime("%Y-%m-%d")
        st.success(f"Payment of {payment_amount} logged for {member_name}.")
    else:
        st.error(f"Member {member_name} not found.")

# Page layout
st.title("Gym Membership Ledger")

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Add Member", "Log Payment", "View Ledger"])

# Tab 1: Add Member
with tab1:
    st.header("Add New Member")
    name = st.text_input("Member Name")
    membership_type = st.selectbox("Membership Type", ["Monthly", "Quarterly", "Yearly"])
    payment_amount = st.number_input("Initial Payment Amount", min_value=0, step=1)
    if st.button("Add Member"):
        if name and membership_type and payment_amount > 0:
            add_member(name, membership_type, payment_amount)
            st.success(f"Member {name} added successfully.")
        else:
            st.error("Please fill in all fields.")

# Tab 2: Log Payment
with tab2:
    st.header("Log Payment")
    member_name = st.text_input("Member Name for Payment")
    payment_amount = st.number_input("Payment Amount", min_value=0, step=1, key="payment")
    if st.button("Log Payment"):
        if member_name and payment_amount > 0:
            log_payment(member_name, payment_amount)
        else:
            st.error("Please fill in all fields.")

# Tab 3: View Ledger
with tab3:
    st.header("Membership Ledger")
    st.dataframe(st.session_state["ledger"])
