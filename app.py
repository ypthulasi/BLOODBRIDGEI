import streamlit as st
import pandas as pd
import sqlite3
# Connect to database
conn = sqlite3.connect("bloodbridge.db", check_same_thread=False)
cursor = conn.cursor()

# Create donors table
cursor.execute("""
CREATE TABLE IF NOT EXISTS donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    blood_group TEXT,
    city TEXT,
    contact TEXT
)
""")

# Create recipient requests table
cursor.execute("""
CREATE TABLE IF NOT EXISTS blood_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_name TEXT,
    blood_group TEXT,
    city TEXT,
    contact TEXT
)
""")

conn.commit()
st.set_page_config(
    page_title="BloodBridge AI",
    page_icon="🩸",
    layout="wide"
)

st.title("🩸 BloodBridge AI")
st.subheader("Smart Blood Bank Management System")

st.write(
    "A centralized platform for blood inventory, "
    "donor registration, and emergency search."
)

st.warning(
    "Hackathon prototype using sample data. "
    "Confirm real availability and compatibility with a qualified blood bank."
)

# Sample inventory
inventory = pd.DataFrame({
    "Blood Group": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "Units Available": [12, 4, 10, 3, 6, 2, 15, 5]
})

# Demo donor records
if "donors" not in st.session_state:
    st.session_state.donors = [
        {
            "Name": "Demo Donor 1",
            "Blood Group": "O+",
            "City": "Bengaluru",
            "Contact": "Demo contact"
        },
        {
            "Name": "Demo Donor 2",
            "Blood Group": "A+",
            "City": "Mysuru",
            "Contact": "Demo contact"
        },
        {
            "Name": "Demo Donor 3",
            "Blood Group": "O-",
            "City": "Bengaluru",
            "Contact": "Demo contact"
        }
    ]

# Dashboard metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Blood Groups", len(inventory))

with col2:
    st.metric(
        "Sample Blood Units",
        int(inventory["Units Available"].sum())
    )

with col3:
    st.metric("Demo Donors", len(st.session_state.donors))

# Navigation tabs
tab1, tab2, tab3,tab4 = st.tabs([
    "📦 Blood Inventory",
    "📝 Donor Registration",
    "🚨 Smart Donor Search",
    "& Recipient Blood Request"
])

# Inventory tab
with tab1:
    st.header("Blood Inventory")

    st.dataframe(inventory, use_container_width=True)

    st.subheader("Inventory Overview")
    st.bar_chart(
        inventory.set_index("Blood Group")["Units Available"]
    )

    required_group = st.selectbox(
        "Select blood group for emergency search",
        inventory["Blood Group"].tolist()
    )

    units_needed = st.number_input(
        "Units requested",
        min_value=1,
        max_value=100,
        value=1
    )

    if st.button("Check Sample Inventory"):
        available = int(
            inventory.loc[
                inventory["Blood Group"] == required_group,
                "Units Available"
            ].iloc[0]
        )

        if available >= units_needed:
            st.success(
                f"Sample inventory lists {available} units of {required_group}."
            )
        else:
            st.warning(
                f"Only {available} sample units of {required_group} are listed."
            )

        st.caption(
            "This is sample data, not live hospital inventory."
        )

# Donor registration tab
with tab2:
    st.header("Register a Donor")
    with st.form("donor_registration"):
        name = st.text_input("Donor name")

        blood_group = st.selectbox(
            "Blood group",
            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            key="donor_group"
        )

        city = st.text_input("City")
        contact = st.text_input("Contact details")

        submitted = st.form_submit_button("Register Donor")
if submitted:
    if name and city and contact:
        st.session_state.donors.append({
            "Name": name,
            "Blood Group": blood_group,
            "City": city,
            "Contact": contact
        })

        cursor.execute("""
            INSERT INTO donors (name, blood_group, city, contact)
            VALUES (?, ?, ?, ?)
        """, (name, blood_group, city, contact))

        conn.commit()

        st.success("Demo donor registered successfully!")

    else:
        st.error("Please complete all fields.")

st.subheader("Registered Demo Donors")
if st.session_state.donors:
    st.dataframe(
        pd.DataFrame(st.session_state.donors))
else:
    st.info("No demo registrered yet.")
        

# Smart donor search tab
with tab3:
    st.header("Find Potential Donors")
    required_group = st.selectbox(
    "Required recipient blood group",
    ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    key="recipient_group"
)

if st.button("Search Donors"):
    donors = st.session_state.donors

    matching_donors = [
        donor for donor in donors
        if donor["Blood Group"] == required_group
    ]

    if matching_donors:
        st.success(
            f"Found {len(matching_donors)} matching donor(s)!"
        )
        st.dataframe(
            pd.DataFrame(matching_donors),
            use_container_width=True
        )
    else:
        st.warning(
            f"No registered demo donors found with blood group {required_group}."
        )
#Recipient Blood Request

with tab3:
    st.header("🩸 Recipient Blood Request")
    st.write("Submit a request if you need blood.")


   # Find donors with the selected blood group
donors = st.session_state.donors

matching_donors = [
    donor for donor in donors
    if donor["Blood Group"] == required_group
]

if matching_donors:
    st.success(f"Found {len(matching_donors)} matching donor(s)!")
    st.dataframe(
        pd.DataFrame(matching_donors),
        use_container_width=True
    )
else:
    st.warning(
        f"No registered demo donors found with blood group {required_group}."
    )
        
#Recipient Blood Request

with tab4:
   st.header("🩸 Recipient Blood Request")
   st.write("Submit a request if you need blood.")

if "blood_requests" not in st.session_state:
    st.session_state.blood_requests = []

with st.form("recipient_request_form"):
    recipient_name = st.text_input("Recipient Name")

    required_blood_group = st.selectbox(
        "Required Blood Group",
        ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        key="request_blood_group"
    )

    recipient_city = st.text_input("City")
    recipient_contact = st.text_input("Contact Number")

    submitted = st.form_submit_button("Submit Blood Request")

    if submitted:
      if (
        recipient_name.strip()
        and recipient_city.strip()
        and recipient_contact.strip()
    ):
        request = {
            "Recipient Name": recipient_name.strip(),
            "Required Blood Group": required_blood_group,
            "City": recipient_city.strip(),
            "Contact": recipient_contact.strip()
        }

        st.session_state.blood_requests.append(request)

        cursor.execute("""
            INSERT INTO blood_requests
            (recipient_name, blood_group, city, contact)
            VALUES (?, ?, ?, ?)
        """, (
            recipient_name.strip(),
            required_blood_group,
            recipient_city.strip(),
            recipient_contact.strip()
        ))

        conn.commit()

        st.success("Blood request submitted successfully! ✅")

    else:
        st.error("Please fill in all the fields.")

st.subheader("📋 Submitted Blood Requests")

if st.session_state.blood_requests:
    st.dataframe(
        pd.DataFrame(st.session_state.blood_requests),
        use_container_width=True
    )
else:
    st.info("No blood requests submitted yet.")