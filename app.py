import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="BloodBridge AI",
    page_icon="🩸",
    layout="wide"
)

# Application title
st.title("🩸 BloodBridge AI")
st.subheader("AI-Powered Smart Blood Bank Management System")

st.write(
    "Connect blood inventory, donor information, and emergency requests "
    "through one simple dashboard."
)

st.info(
    "Demo application: inventory and donor information are sample data. "
    "Confirm real availability and compatibility with a qualified blood bank."
)

# Sample inventory
inventory = pd.DataFrame({
    "Blood Group": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "Units Available": [12, 4, 10, 3, 6, 2, 15, 5]
})

# Dashboard metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("Blood Groups Tracked", len(inventory))

with col2:
    st.metric("Total Sample Units", int(inventory["Units Available"].sum()))

# Inventory table
st.header("📦 Blood Inventory")
st.dataframe(inventory, use_container_width=True)

# Inventory chart
st.header("📊 Inventory Overview")
st.bar_chart(inventory.set_index("Blood Group")["Units Available"])

# Emergency search
st.header("🚨 Emergency Blood Search")

blood_group = st.selectbox(
    "Select required blood group",
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
            inventory["Blood Group"] == blood_group,
            "Units Available"
        ].iloc[0]
    )

    st.write(f"Requested blood group: **{blood_group}**")
    st.write(f"Units requested: **{units_needed}**")
    st.write(f"Units in sample inventory: **{available}**")

    if available >= units_needed:
        st.success("The sample inventory has enough units.")
    else:
        st.warning("The sample inventory has insufficient units.")

    st.caption(
        "This is a software demonstration, not a live blood availability "
        "check. Contact a real blood bank to confirm availability."
    )

st.divider()
st.caption("BloodBridge AI | Hackathon Prototype")