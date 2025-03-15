import streamlit as st

# Title
st.title("Up AI Follow-Up App (Demo)")

# Sidebar Navigation
page = st.sidebar.selectbox("Navigation", ["Dashboard", "Settings"])

# Dashboard Page
if page == "Dashboard":
    st.header("Lead Dashboard")
    leads = [
        {"id": 1, "name": "John Doe", "status": "Pending"},
        {"id": 2, "name": "Jane Smith", "status": "Follow-Up"},
        {"id": 3, "name": "Mike Johnson", "status": "Closed"},
    ]
    
    for lead in leads:
        with st.expander(f"Lead {lead['id']}: {lead['name']}"):
            st.write(f"Status: {lead['status']}")
            st.button(f"Call {lead['name']}")

# Settings Page
elif page == "Settings":
    st.header("Settings (Mockup)")
    st.write("No real settings yet.")
