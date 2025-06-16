import streamlit as st
import pandas as pd

# --- Session Setup ---
if "role" not in st.session_state:
    st.session_state.role = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "project_data" not in st.session_state:
    st.session_state.project_data = None
if "selected_brand" not in st.session_state:
    st.session_state.selected_brand = None
if "saved_reviews" not in st.session_state:
    st.session_state.saved_reviews = {}

# --- Sticky Header and Sidebar Styling ---
st.markdown("""
    <style>
    .sticky-header {
        position: sticky;
        top: 0;
        background-color: #ffffff;
        padding: 1rem 0;
        z-index: 100;
        border-bottom: 1px solid #ddd;
    }
    .floating-panel {
        position: fixed;
        top: 100px;
        right: 20px;
        width: 230px;
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# --- Login Page ---
if st.session_state.page == "login":
    st.title("🔐 FIDO Review Tool")
    st.subheader("Select your role to begin:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 Reviewer"):
            st.session_state.role = "reviewer"
            st.session_state.page = "brand_list"
    with col2:
        if st.button("🛠️ Admin"):
            st.session_state.role = "admin"
            st.session_state.page = "upload"

# --- Admin Upload Page ---
if st.session_state.page == "upload" and st.session_state.role == "admin":
    st.title("🛠️ Admin: Upload FIDO File")
    uploaded_file = st.file_uploader("Upload CSV File", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.project_data = df
        st.success("✅ File uploaded. Proceed to review projects.")
        st.session_state.page = "brand_list"

# --- Brand List Page ---
if st.session_state.page == "brand_list":
    st.title("📋 Brand Review Projects")
    df = st.session_state.project_data
    if df is not None:
        brand_list = sorted(df["BRAND"].dropna().unique().tolist())
        for brand in brand_list:
            if st.button(f"🔎 Review '{brand}'", use_container_width=True):
                st.session_state.selected_brand = brand
                st.session_state.page = "brand_review"
                break
    else:
        st.warning("No data loaded. Please ask an admin to upload a file.")

# --- Brand Review Page ---
if st.session_state.page == "brand_review":
    df = st.session_state.project_data
    brand = st.session_state.selected_brand
    brand_df = df[df["BRAND"] == brand].copy().reset_index(drop=True)

    # Sticky Header
    st.markdown(f"<div class='sticky-header'><h2>🧾 Reviewing Brand: {brand}</h2></div>", unsafe_allow_html=True)

    # Floating control panel
    with st.sidebar:
        st.markdown("### 🛠️ Controls")
        # --- UPC Lookup Sidebar Tool ---
st.markdown("### 🔎 Search UPC on BarcodeLookup")
upc_input = st.text_input("Enter UPC", key="upc_lookup_input")
if upc_input:
    upc_url = f"https://barcodelookup1.streamlit.app/?search={upc_input}"
    st.markdown(f"[🔗 Search '{upc_input}' on BarcodeLookup]({upc_url})", unsafe_allow_html=True)
        if st.button("💾 Save All"):
            for i, row in brand_df.iterrows():
                fido = row["FIDO"]
                st.session_state.saved_reviews[fido] = {
                    "FIDO": fido,
                    "BARCODE": row["BARCODE"],
                    "Original Description": row["DESCRIPTION"],
                    "Updated Description": st.session_state.get(f"desc_{i}", row["DESCRIPTION"]),
                    "Original Category": row["CATEGORY"],
                    "Updated Category": st.session_state.get(f"cat_{i}", row["CATEGORY"]),
                    "Original Brand": row["BRAND"],
                    "Updated Brand": st.session_state.get(f"brand_{i}", row["BRAND"]),
                    "BRAND_ID": row.get("BRAND_ID", ""),
                    "Is Brand ID Null?": row["Is Brand ID Null?"],
                    "GMV L365d from Data Pull Date": row["GMV L365d from Data Pull Date"],
                    "No Change": st.session_state.get(f"correct_{i}", False),
                    "Reviewer Notes": st.session_state.get(f"note_{i}", "")
                }
            st.success("✅ All changes saved.")

        if st.session_state.role == "admin" and st.session_state.saved_reviews:
            export_df = pd.DataFrame(st.session_state.saved_reviews.values())
            csv = export_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Reviewed Data",
                data=csv,
                file_name=f"Reviewed_{brand.replace(' ', '_')}_FIDO.csv",
                mime="text/csv"
            )

        if st.button("🔙 Back to Brand List"):
            st.session_state.page = "brand_list"
            st.session_state.selected_brand = None

    # Main FIDO Display Loop
    for i, row in brand_df.iterrows():
        st.markdown("----")
        st.subheader(f"FIDO: {row['FIDO']}")
        st.text(f"UPC: {row['BARCODE']}")
        st.text(f"Brand ID: {row.get('BRAND_ID', 'N/A')}")
        st.text(f"Original Brand: {row['BRAND']}")
        st.text(f"Category: {row['CATEGORY']}")
        st.text(f"Description: {row['DESCRIPTION']}")
        st.text(f"GMV: {row['GMV L365d from Data Pull Date']}")
        st.text(f"Brand ID Status: {row['Is Brand ID Null?']}")

        # Inputs
        updated_desc = st.text_area(f"📝 Updated Description", value=row["DESCRIPTION"], key=f"desc_{i}")
        updated_cat = st.text_input(f"📦 Updated Category", value=row["CATEGORY"], key=f"cat_{i}")
        updated_brand = st.text_input(f"🏷️ Updated Brand", value=row["BRAND"], key=f"brand_{i}")
        mark_correct = st.checkbox("✅ No Change", key=f"correct_{i}")
        reviewer_note = st.text_input("🗒️ Notes", key=f"note_{i}")

        if st.button(f"💾 Save FIDO {row['FIDO']}", key=f"save_{i}"):
            st.session_state.saved_reviews[row["FIDO"]] = {
                "FIDO": row["FIDO"],
                "BARCODE": row["BARCODE"],
                "Original Description": row["DESCRIPTION"],
                "Updated Description": updated_desc,
                "Original Category": row["CATEGORY"],
                "Updated Category": updated_cat,
                "Original Brand": row["BRAND"],
                "Updated Brand": updated_brand,
                "BRAND_ID": row.get("BRAND_ID", ""),
                "Is Brand ID Null?": row["Is Brand ID Null?"],
                "GMV L365d from Data Pull Date": row["GMV L365d from Data Pull Date"],
                "No Change": mark_correct,
                "Reviewer Notes": reviewer_note
            }
            st.success(f"✅ Saved {row['FIDO']}")
