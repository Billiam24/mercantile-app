import json
import os
import streamlit as st
from ava import ask_ava
from database import add_inventory, get_inventory


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Medley Mercantile - Homestead Hub",
    page_icon="🏡",
    layout="wide",
)





# =========================================================
# FILE PATHS FOR DATA STORAGE
# =========================================================

NOTES_FILE = "homestead_notes.json"
MEDICAL_FILE = "animal_medical_logs.json"
INVENTORY_FILE = "inventory.json"


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    return []


def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# =========================================================
# APP HEADER
# =========================================================

st.title("🏡 Medley Mercantile Command Center")
st.markdown(
    "Growing Home, Together. Manage animals, projects, and inventory."
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

menu = st.sidebar.selectbox(
    "Navigation Menu",
    [
        "🏡 Dashboard",
        "🌱 Garden",
        "🌦️ Weather",
        "🐓 Animals",
        "💉 Animal Medical Logs",
        "📋 Notes & Projects",
        "📦 Inventory",
        "💰 Farmers Market",
        "🛒 Purchases",
        "🏪 Medley Mercantile",
        "🤖 AI Assistant (Ava)",
    ],
)


# =========================================================
# 1. DASHBOARD
# =========================================================

if menu == "🏡 Dashboard":

    st.header("🏡 Homestead Dashboard")

    notes_list = load_data(NOTES_FILE)
    med_list = load_data(MEDICAL_FILE)
    inventory = load_data(INVENTORY_FILE)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📝 Projects & Notes",
            len(notes_list)
        )

    with col2:
        st.metric(
            "🐓 Medical Records",
            len(med_list)
        )

    with col3:
        st.metric(
            "📦 Inventory Items",
            len(inventory)
        )

    st.divider()

    st.subheader("Welcome to Medley Mercantile")

    st.write(
        """
        This is your homestead command center.

        Use the navigation menu on the left to manage your
        animals, projects, inventory, and eventually the
        broader Medley Mercantile business.
        """
    )

    st.info(
        "🚧 More dashboard features will be added as the app grows."
    )


# =========================================================
# 2. GARDEN
# =========================================================

elif menu == "🌱 Garden":

    st.header("🌱 Garden")

    st.info(
        "Garden management is coming next. "
        "This section will eventually track crops, planting dates, "
        "harvests, supplies, and garden projects."
    )


# =========================================================
# 3. WEATHER
# =========================================================

elif menu == "🌦️ Weather":

    st.header("🌦️ Weather")

    st.info(
        "Weather integration will be added later using a weather API."
    )


# =========================================================
# 4. ANIMALS
# =========================================================

elif menu == "🐓 Animals":

    st.header("🐓 Animals")

    st.info(
        "Animal management is coming next. "
        "This section will eventually track individual animals, "
        "species, breeds, ages, feeding, housing, and other records."
    )


# =========================================================
# 5. ANIMAL MEDICAL LOGS
# =========================================================

elif menu == "💉 Animal Medical Logs":

    st.subheader("Animal Medical Administration Log")

    with st.form("medical_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:

            animal_name = st.text_input(
                "Animal Name / ID"
            )

            medication = st.text_input(
                "Medication / Treatment Name"
            )

        with col2:

            dosage = st.text_input(
                "Dosage (e.g., 2cc, 1 pill)"
            )

            date_given = st.date_input(
                "Date Administered"
            )

        notes = st.text_area(
            "Symptoms / Notes / Follow-up"
        )

        submit_med = st.form_submit_button(
            "Log Treatment"
        )

        if submit_med and animal_name and medication:

            med_list = load_data(MEDICAL_FILE)

            med_list.append(
                {
                    "animal": animal_name,
                    "medication": medication,
                    "dosage": dosage,
                    "date": str(date_given),
                    "notes": notes,
                }
            )

            save_data(
                MEDICAL_FILE,
                med_list
            )

            st.success(
                "Medical log saved!"
            )

        elif submit_med:

            st.error(
                "Please fill in at least the Animal Name and Medication."
            )

    st.divider()

    st.subheader("Medical History Records")

    med_list = load_data(MEDICAL_FILE)

    if med_list:

        for item in reversed(med_list):

            st.markdown(
                f"**{item['date']} - {item['animal']}** | "
                f"Treated with: **{item['medication']}** "
                f"({item['dosage']})"
            )

            if item["notes"]:

                st.caption(
                    f"Notes: {item['notes']}"
                )

            st.markdown("---")

    else:

        st.info(
            "No medical logs recorded yet."
        )


# =========================================================
# 6. NOTES & PROJECTS
# =========================================================

elif menu == "📋 Notes & Projects":

    st.subheader("Homestead Projects & Notes")

    with st.form(
        "project_form",
        clear_on_submit=True
    ):

        title = st.text_input(
            "Project / Note Title"
        )

        category = st.selectbox(
            "Category",
            [
                "Garden",
                "Animals",
                "Infrastructure",
                "General",
            ],
        )

        details = st.text_area(
            "Details / Steps / Notes"
        )

        submit_project = st.form_submit_button(
            "Save Note/Project"
        )

        if submit_project and title:

            notes_list = load_data(
                NOTES_FILE
            )

            notes_list.append(
                {
                    "title": title,
                    "category": category,
                    "details": details,
                }
            )

            save_data(
                NOTES_FILE,
                notes_list
            )

            st.success(
                "Project/Note saved successfully!"
            )

        elif submit_project:

            st.error(
                "Please provide a title."
            )

    st.divider()

    st.subheader(
        "Current Notes & Projects"
    )

    notes_list = load_data(
        NOTES_FILE
    )

    if notes_list:

        for item in notes_list:

            with st.expander(
                f"{item['category']}: {item['title']}"
            ):

                st.write(
                    item["details"]
                )

    else:

        st.info(
            "No notes or projects logged yet."
        )


# =========================================================
# 7. INVENTORY
# =========================================================

elif menu == "📦 Inventory":

    st.subheader(
        "Property & Parts Inventory"
    )

    with st.form(
        "inventory_form",
        clear_on_submit=True
    ):

        item_name = st.text_input(
            "Item / Part Name"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        location = st.text_input(
            "Location / Shed / Shelf"
        )

        submit_inv = st.form_submit_button(
            "Add Item"
        )

        if submit_inv and item_name:

            add_inventory(
                item_name,
                quantity,
                location,
                ""
            )

            st.success(
                "Inventory item added!"
            )

        elif submit_inv:

            st.error(
                "Please provide an item name."
            )

    st.divider()

    st.subheader(
        "Current Inventory List"
    ) 

    inventory = get_inventory()

    if inventory:

        for item in inventory:

            st.write(
                f"🔹 **{item['item_name']}** "
                f"(Qty: {item['quantity']}) — "
                f"Located at: {item['location']}"
            )

    else:

        st.info(
            "No inventory items logged yet."
        )


# =========================================================
# 8. FARMERS MARKET
# =========================================================

elif menu == "💰 Farmers Market":

    st.header("💰 Farmers Market")

    st.info(
        "Farmers Market tools are coming next. "
        "This section can eventually track products, prices, "
        "customers, sales, and market inventory."
    )


# =========================================================
# 9. PURCHASES
# =========================================================

elif menu == "🛒 Purchases":

    st.header("🛒 Purchases")

    st.info(
        "Purchase tracking is coming next. "
        "This section can eventually track purchases, costs, "
        "suppliers, receipts, and expenses."
    )


# =========================================================
# 10. MEDLEY MERCANTILE
# =========================================================

elif menu == "🏪 Medley Mercantile":

    st.header("🏪 Medley Mercantile")

    st.info(
        "The Medley Mercantile business center is coming next. "
        "This will eventually connect the homestead side of the app "
        "with the actual business."
    )


# =========================================================
# 11. AI ASSISTANT — AVA
# =========================================================

elif menu == "🤖 AI Assistant (Ava)":

    st.subheader(
        "💬 Chat with Ava - Homestead & Livestock Assistant"
    )

    st.caption(
        "Ava is powered by Groq AI."
    )

    if "ava_messages" not in st.session_state:

        st.session_state.ava_messages = [
            {
                "role": "system",
                "content": (
                    "You are Ava, a technical livestock and homestead "
                    "reference assistant. Provide practical, educational "
                    "information about homesteading, livestock, animal "
                    "care, gardening, and related topics. Clearly "
                    "distinguish general educational information from "
                    "situations requiring a veterinarian or other "
                    "qualified professional."
                ),
            }
        ]

    for message in st.session_state.ava_messages:

        if message["role"] != "system":

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

    if prompt := st.chat_input(
        "Ask Ava a question..."
    ):

        st.session_state.ava_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):

            st.markdown(
                prompt
            )

        with st.chat_message("assistant"):

            response_placeholder = st.empty()

            response_placeholder.markdown(
                "Ava is thinking..."
            )
        try:
            response = ask_ava(
                user_message=prompt,
                conversation=st.session_state.ava_messages[:-1]
            )

            response_placeholder.markdown(response)

            st.session_state.ava_messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

        except Exception as e:
            response_placeholder.error(
                f"Error connecting to Ava: {e}"
            )