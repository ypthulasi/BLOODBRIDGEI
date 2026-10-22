import streamlit as st
import pandas as pd

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
tab1, tab2, tab3 = st.tabs([
    "📦 Blood Inventory",
    "📝 Donor Registration",
    "🚨 Smart Donor Search"
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
            if name.strip() and city.strip() and contact.strip():
                st.session_state.donors.append({
                    "Name": name.strip(),
                    "Blood Group": blood_group,
                    "City": city.strip(),
                    "Contact": contact.strip()
                })

                st.success("Demo donor registered successfully!")
            else:
                st.error("Please complete all fields.")

    st.subheader("Registered Demo Donors")

    st.dataframe(
        pd.DataFrame(st.session_state.donors),
        use_container_width=True
    )

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

    # Find donors with the selected blood group
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
