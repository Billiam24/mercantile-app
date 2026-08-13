import json
import os
from datetime import datetime

import streamlit as st

from ava import ask_ava
from database import add_inventory, get_inventory


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Medley Mercantile | Command Center",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# LOCAL FILES — legacy records remain safe while Supabase
# becomes the cloud foundation for inventory.
# =========================================================

NOTES_FILE = "homestead_notes.json"
MEDICAL_FILE = "animal_medical_logs.json"


# =========================================================
# VISUAL SYSTEM
# =========================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128,128,128,.18);
        }

        .hero {
            padding: 1.35rem 1.5rem;
            border-radius: 18px;
            background: linear-gradient(
                135deg,
                rgba(39, 72, 56, .16),
                rgba(214, 170, 91, .12)
            );
            border: 1px solid rgba(128,128,128,.18);
            margin-bottom: 1.25rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 2.35rem;
            letter-spacing: -.03em;
        }

        .hero p {
            margin: .35rem 0 0 0;
            opacity: .78;
            font-size: 1.02rem;
        }

        .section-title {
            font-size: 1.45rem;
            font-weight: 700;
            margin: .5rem 0 .85rem 0;
        }

        .status-pill {
            display: inline-block;
            padding: .28rem .65rem;
            border-radius: 999px;
            font-size: .78rem;
            font-weight: 700;
            background: rgba(46, 125, 50, .13);
            border: 1px solid rgba(46, 125, 50, .25);
        }

        .small-muted {
            opacity: .68;
            font-size: .88rem;
        }

        div[data-testid="stMetric"] {
            padding: .85rem;
            border-radius: 14px;
            border: 1px solid rgba(128,128,128,.16);
            background: rgba(128,128,128,.045);
        }

        .feature-card {
            padding: 1rem;
            border-radius: 15px;
            border: 1px solid rgba(128,128,128,.16);
            min-height: 130px;
            background: rgba(128,128,128,.035);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def load_data(file_path):
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def safe_inventory():
    """Return cloud inventory without crashing the whole app."""
    try:
        return get_inventory() or []
    except Exception:
        return []


def inventory_status():
    """Small cloud health check for the dashboard."""
    try:
        rows = get_inventory()
        return True, len(rows or [])
    except Exception:
        return False, 0


def homestead_context():
    """Give Ava useful live application context without exposing secrets."""
    notes = load_data(NOTES_FILE)
    medical = load_data(MEDICAL_FILE)
    inventory = safe_inventory()

    recent_notes = notes[-8:]
    recent_medical = medical[-8:]
    recent_inventory = inventory[-15:]

    return json.dumps(
        {
            "inventory": recent_inventory,
            "recent_projects_and_notes": recent_notes,
            "recent_medical_logs": recent_medical,
        },
        indent=2,
        default=str,
    )


def set_page(page):
    st.rerun()


# =========================================================
# NAVIGATION
# =========================================================

PAGES = [
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
]

if "nav" not in st.session_state:
    st.session_state.nav = PAGES[0]

with st.sidebar:
    st.markdown("## 🏡 Medley Mercantile")
    st.caption("Growing Home, Together.")

    st.divider()

    menu = st.radio(
        "Command Center",
        PAGES,
        key="nav",
        label_visibility="collapsed",
    )

    st.divider()

    cloud_ok, cloud_count = inventory_status()

    if cloud_ok:
        st.markdown(
            f'<span class="status-pill">☁️ Cloud online</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"{cloud_count} inventory item(s) in Supabase")
    else:
        st.markdown(
            '<span class="status-pill">⚠️ Cloud needs attention</span>',
            unsafe_allow_html=True,
        )

    st.caption("Medley Mercantile • Command Center")


# =========================================================
# GLOBAL HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>🏡 Medley Mercantile Command Center</h1>
        <p>Growing Home, Together. One place for the homestead, the
        animals, the projects, and the business.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 1. DASHBOARD
# =========================================================

if menu == "🏡 Dashboard":

    notes = load_data(NOTES_FILE)
    medical = load_data(MEDICAL_FILE)
    inventory = safe_inventory()
    cloud_ok, cloud_count = inventory_status()

    st.markdown('<div class="section-title">Today at a glance</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📋 Projects & Notes", len(notes))

    with c2:
        st.metric("💉 Medical Records", len(medical))

    with c3:
        st.metric("📦 Cloud Inventory", cloud_count)

    with c4:
        st.metric("☁️ Cloud Status", "Online" if cloud_ok else "Offline")

    st.divider()

    left, right = st.columns([1.55, 1])

    with left:
        st.markdown("### ⚡ Quick actions")

        q1, q2, q3 = st.columns(3)

        with q1:
            if st.button("📦 Add Inventory", use_container_width=True):
                set_page("📦 Inventory")
                st.rerun()

        with q2:
            if st.button("📋 New Project", use_container_width=True):
                set_page("📋 Notes & Projects")
                st.rerun()

        with q3:
            if st.button("💉 Medical Log", use_container_width=True):
                set_page("💉 Animal Medical Logs")
                st.rerun()

        st.markdown("### 🧭 Command areas")

        a, b = st.columns(2)

        with a:
            st.markdown(
                """
                <div class="feature-card">
                    <b>🐓 Homestead</b><br>
                    <span class="small-muted">
                    Animals, garden, medical records, projects,
                    weather, and supplies.
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with b:
            st.markdown(
                """
                <div class="feature-card">
                    <b>🏪 Business</b><br>
                    <span class="small-muted">
                    Farmers Market, purchases, products, sales,
                    and Medley Mercantile operations.
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("### 🕒 Recent activity")

        activity = []

        for item in reversed(notes[-5:]):
            activity.append(
                f"📋 **{item.get('title', 'Untitled')}**"
            )

        for item in reversed(inventory[-5:]):
            activity.append(
                f"📦 **{item.get('item_name', 'Inventory item')}**"
            )

        if activity:
            for entry in activity[:8]:
                st.write(entry)
        else:
            st.info("Your command center is ready. Add your first record.")


# =========================================================
# 2. GARDEN
# =========================================================

elif menu == "🌱 Garden":

    st.header("🌱 Garden")
    st.caption("Plan now. Plant well. Harvest with purpose.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Crop planning", "Ready")

    with c2:
        st.metric("Planting calendar", "Next")

    with c3:
        st.metric("Harvest records", "Next")

    st.info(
        "The garden module is staged for the next data-model upgrade. "
        "The navigation and command-center foundation are already in place."
    )


# =========================================================
# 3. WEATHER
# =========================================================

elif menu == "🌦️ Weather":

    st.header("🌦️ Weather")
    st.caption("Weather-aware planning is coming into the command center.")

    st.info(
        "Weather API integration is intentionally kept separate from "
        "the core app so a provider can be added without destabilizing "
        "your homestead records."
    )

    st.markdown("### Planned weather intelligence")
    st.write(
        "Forecast → frost/rain alerts → animal and garden planning → "
        "Ava context."
    )


# =========================================================
# 4. ANIMALS
# =========================================================

elif menu == "🐓 Animals":

    st.header("🐓 Animals")
    st.caption("The animals are the heart of the homestead.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Animal registry", "Next")

    with c2:
        st.metric("Feeding records", "Next")

    with c3:
        st.metric("Housing records", "Next")

    st.info(
        "The animal registry is the next major cloud-data module. "
        "We can add individual animals, species, breed, age, housing, "
        "feeding, and links to medical records without changing Ava."
    )


# =========================================================
# 5. ANIMAL MEDICAL LOGS
# =========================================================

elif menu == "💉 Animal Medical Logs":

    st.header("💉 Animal Medical Records")
    st.caption("Keep treatments, observations, and follow-ups organized.")

    with st.form("medical_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            animal_name = st.text_input("Animal Name / ID")
            medication = st.text_input("Medication / Treatment")

        with col2:
            dosage = st.text_input("Dosage")
            date_given = st.date_input("Date Administered")

        notes = st.text_area("Symptoms / Notes / Follow-up")

        submit_med = st.form_submit_button(
            "💾 Log Treatment",
            use_container_width=True,
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
                    "logged_at": datetime.now().isoformat(timespec="seconds"),
                }
            )

            save_data(MEDICAL_FILE, med_list)
            st.success("Medical log saved.")

        elif submit_med:
            st.error("Please provide the animal and treatment.")

    st.divider()
    st.subheader("Medical History")

    med_list = load_data(MEDICAL_FILE)

    if med_list:
        for item in reversed(med_list):
            with st.expander(
                f"{item.get('date', '')} • "
                f"{item.get('animal', 'Unknown')} • "
                f"{item.get('medication', 'Treatment')}"
            ):
                st.write(f"**Dosage:** {item.get('dosage', '')}")
                st.write(f"**Notes:** {item.get('notes', '') or '—'}")
    else:
        st.info("No medical logs recorded yet.")


# =========================================================
# 6. NOTES & PROJECTS
# =========================================================

elif menu == "📋 Notes & Projects":

    st.header("📋 Notes & Projects")
    st.caption("Turn ideas into work that actually gets finished.")

    with st.form("project_form", clear_on_submit=True):

        title = st.text_input("Project / Note Title")

        category = st.selectbox(
            "Category",
            ["Garden", "Animals", "Infrastructure", "Business", "General"],
        )

        details = st.text_area("Details / Steps / Notes")

        submit_project = st.form_submit_button(
            "💾 Save Project",
            use_container_width=True,
        )

        if submit_project and title:
            notes = load_data(NOTES_FILE)

            notes.append(
                {
                    "title": title,
                    "category": category,
                    "details": details,
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                }
            )

            save_data(NOTES_FILE, notes)
            st.success("Project saved.")

        elif submit_project:
            st.error("Please provide a title.")

    st.divider()
    st.subheader("Current Projects")

    notes = load_data(NOTES_FILE)

    if notes:
        for item in reversed(notes):
            with st.expander(
                f"{item.get('category', 'General')} • "
                f"{item.get('title', 'Untitled')}"
            ):
                st.write(item.get("details", ""))
    else:
        st.info("No projects or notes logged yet.")


# =========================================================
# 7. INVENTORY — SUPABASE / CLOUD
# =========================================================

elif menu == "📦 Inventory":

    st.header("📦 Cloud Inventory")
    st.caption("Inventory is backed by Supabase so it can become a shared, multi-device source of truth.")

    inventory = safe_inventory()

    with st.form("inventory_form", clear_on_submit=True):

        c1, c2 = st.columns(2)

        with c1:
            item_name = st.text_input("Item / Part Name")
            location = st.text_input("Location / Shed / Shelf")

        with c2:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                step=1,
            )
            item_notes = st.text_input("Notes")

        submit_inv = st.form_submit_button(
            "☁️ Add to Cloud Inventory",
            use_container_width=True,
        )

        if submit_inv and item_name:
            try:
                add_inventory(
                    item_name,
                    int(quantity),
                    location,
                    item_notes,
                )
                st.success("Inventory item saved to Supabase.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not save inventory item: {exc}")

        elif submit_inv:
            st.error("Please provide an item name.")

    st.divider()

    if inventory:
        search = st.text_input(
            "🔎 Search inventory",
            placeholder="Search item, location, or notes...",
        ).strip().lower()

        filtered = []

        for item in inventory:
            haystack = " ".join(
                str(item.get(key, ""))
                for key in ("item_name", "location", "notes")
            ).lower()

            if not search or search in haystack:
                filtered.append(item)

        st.write(f"Showing **{len(filtered)}** of **{len(inventory)}** items.")

        for item in filtered:
            c1, c2, c3 = st.columns([2.2, 1, 1.5])

            with c1:
                st.markdown(
                    f"**{item.get('item_name', 'Unnamed item')}**"
                )

            with c2:
                st.write(f"Qty: {item.get('quantity', 0)}")

            with c3:
                st.caption(item.get("location") or "No location")
    else:
        st.info("No inventory items are stored in the cloud yet.")


# =========================================================
# 8. FARMERS MARKET
# =========================================================

elif menu == "💰 Farmers Market":

    st.header("💰 Farmers Market")
    st.caption("From homestead production to a real sales workflow.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Products", "Next")

    with c2:
        st.metric("Sales", "Next")

    with c3:
        st.metric("Revenue", "Next")

    st.info(
        "This module is staged for the business data layer: products, "
        "prices, customers, sales, and market inventory."
    )


# =========================================================
# 9. PURCHASES
# =========================================================

elif menu == "🛒 Purchases":

    st.header("🛒 Purchases")
    st.caption("Track what comes in, what it costs, and where it came from.")

    st.info(
        "Purchase tracking is staged for the cloud business layer: "
        "suppliers, costs, receipts, categories, and expenses."
    )


# =========================================================
# 10. MEDLEY MERCANTILE
# =========================================================

elif menu == "🏪 Medley Mercantile":

    st.header("🏪 Medley Mercantile")
    st.caption("The business side of the homestead.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Products", "Next")

    with c2:
        st.metric("Orders", "Next")

    with c3:
        st.metric("Business records", "Next")

    st.info(
        "The business center will connect products, inventory, purchases, "
        "farmers-market activity, and eventually sales."
    )


# =========================================================
# 11. AVA — CENTRAL AI ASSISTANT
# =========================================================

elif menu == "🤖 AI Assistant (Ava)":

    st.header("🤖 Ava")
    st.caption(
        "Homestead intelligence powered by Groq AI • "
        "Ava can use the application's current records as context."
    )

    context = homestead_context()

    if "ava_messages" not in st.session_state:
        st.session_state.ava_messages = []

    top1, top2 = st.columns([4, 1])

    with top1:
        st.markdown("### 💬 Homestead & Livestock Assistant")

    with top2:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.ava_messages = []
            st.rerun()

    for message in st.session_state.ava_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Ava about the homestead..."):

        st.session_state.ava_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Ava is thinking...")

            try:
                response = ask_ava(
                    user_message=prompt,
                    context=context,
                    conversation=st.session_state.ava_messages[:-1],
                )

                placeholder.markdown(response)

                st.session_state.ava_messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

            except Exception as exc:
                placeholder.error(f"Error connecting to Ava: {exc}")
