import os
os.environ["XDG_CONFIG_HOME"] = "/tmp"
os.environ["STREAMLIT_HOME"] = "/tmp"

import streamlit as st

from ui_components import display_header
from utils.lang_detect import detect_language
import csv
from datetime import datetime
import os
import pandas as pd

st.set_page_config(page_title="BhashaVerse", layout="centered")
display_header()

# Ensure data file exists
os.makedirs("data", exist_ok=True)
csv_path = "data/corpus.csv"
if not os.path.exists(csv_path):
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Proverb", "Meaning", "Language", "Timestamp"])

# Submission Form
with st.form("proverb_form"):
    proverb = st.text_area("Enter your proverb or folk saying in your native language:")
    meaning = st.text_area("Write a short meaning or story behind it (optional):")
    manual_lang = st.selectbox("Select language (optional)", ["", "Telugu", "Tamil", "Hindi", "Kannada", "Other"])
    submit = st.form_submit_button("Submit")

if submit:
    if not proverb.strip():
        st.error("⚠️ Proverb cannot be empty.")
    else:
        lang = manual_lang if manual_lang else detect_language(proverb)
        with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([proverb.strip(), meaning.strip(), lang, datetime.now().isoformat()])
        st.success(f"✅ Thank you! Your proverb has been recorded in **{lang}**.")

# 🔍 Display submitted proverbs
st.markdown("## 📜 Submitted Proverbs")

try:
    df = pd.read_csv(csv_path)

    # Filter dropdown
    lang_filter = st.selectbox("Filter by language", ["All"] + sorted(df["Language"].dropna().unique()))

    if lang_filter != "All":
        df = df[df["Language"] == lang_filter]

    # Display the table
    st.dataframe(df[["Proverb", "Meaning", "Language", "Timestamp"]].sort_values(by="Timestamp", ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"Error loading submitted proverbs: {e}")


# Optional: Download corpus CSV
st.markdown("### 📥 Download All Proverbs")
with open(csv_path, "rb") as f:
    st.download_button(
        label="Download Corpus (CSV)",
        data=f,
        file_name="bhashaverse_corpus.csv",
        mime="text/csv"
    )
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

