import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )


def add_inventory(item_name, quantity=1, location="", notes=""):
    supabase = get_supabase()

    return supabase.table("inventory").insert({
        "item_name": item_name,
        "quantity": quantity,
        "location": location,
        "notes": notes
    }).execute()


def get_inventory():
    supabase = get_supabase()

    response = supabase.table("inventory").select("*").execute()

    return response.data