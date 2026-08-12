import streamlit as st
from datetime import datetime


def render_dashboard():

    st.title("🏡 Medley Mercantile Homestead")
    st.caption("Growing Home, Together.")

    st.divider()

    # --------------------------------------------------
    # QUICK OVERVIEW
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌱 Garden", "Coming Soon")

    with col2:
        st.metric("🐔 Animals", "Coming Soon")

    with col3:
        st.metric("🌦️ Weather", "Live Soon")

    with col4:
        st.metric("🛒 Business", "Coming Soon")

    st.divider()

    # --------------------------------------------------
    # HOMESTEAD QUICK ACTIONS
    # --------------------------------------------------

    st.subheader("🌿 Homestead Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🌱 Garden", use_container_width=True):
            st.info("Garden management will be added here.")

    with col2:
        if st.button("🐔 Animals", use_container_width=True):
            st.info("Animal management will be added here.")

    with col3:
        if st.button("🌦️ Weather", use_container_width=True):
            st.info("Live weather and radar will be added here.")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📦 Inventory", use_container_width=True):
            st.info("Inventory management will be added here.")

    with col2:
        if st.button("🧺 Farmers Market", use_container_width=True):
            st.info("Farmers market sales tracking will be added here.")

    with col3:
        if st.button("🏪 Medley Mercantile", use_container_width=True):
            st.info("Business management will be added here.")

    st.divider()

    # --------------------------------------------------
    # TODAY
    # --------------------------------------------------

    st.subheader("📅 Today")

    today = datetime.now().strftime("%A, %B %d, %Y")

    st.info(f"Today is **{today}**.")

    st.write(
        "This will eventually become your daily homestead command center — "
        "tasks, garden work, animal care, weather alerts, harvests, sales, "
        "inventory and business activity all in one place."
    )

    st.divider()

    # --------------------------------------------------
    # UPCOMING FEATURES
    # --------------------------------------------------

    st.subheader("🚜 Homestead Command Center")

    st.markdown(
        """
        **Planned systems**

        🌱 **Garden Manager**  
        Planting dates • Harvest dates • Maintenance • Crop notes • Growing calendar

        🌦️ **Weather Center**  
        Live conditions • Radar • Precipitation • Wind • Storm information • Alerts

        🐓 **Animal Manager**  
        Animal records • Medical logs • Feeding • Breeding • Care schedules

        📦 **Inventory**  
        Homestead supplies • Feed • Parts • Tools • Household inventory

        🧺 **Farmers Market**  
        Products • Sales • Customers • Revenue • Expenses • Market history

        🏪 **Medley Mercantile**  
        Products • Orders • Business records • Sales • Inventory • Business dashboard

        🤖 **Ava AI**  
        Homestead questions • Garden help • Animal questions • Planning assistance
        """
    )