import streamlit as st
import pandas as pd

st.set_page_config(page_title="FIDO Brand Review Projects", layout="wide")

# Session state to manage uploaded file and project view
if "project_data" not in st.session_state:
    st.session_state.project_data = None
if "selected_brand" not in st.session_state:
    st.session_state.selected_brand = None

st.title("🗂️ FIDO Review Project Dashboard")

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("📤 Upload a FIDO Review File (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.project_data = df
    st.session_state.selected_brand = None  # Reset on new upload

# Step 2: Show brand list if file uploaded
if st.session_state.project_data is not None and st.session_state.selected_brand is None:
    df = st.session_state.project_data
    brand_list = sorted(df["BRAND"].dropna().unique().tolist())
    st.markdown("### 📋 Available Brand Projects")
    for brand in brand_list:
        if st.button(f"🔎 Review '{brand}'"):
            st.session_state.selected_brand = brand
            break

# Step 3: Show review UI for selected brand
if st.session_state.project_data is not None and st.session_state.selected_brand is not None:
    df = st.session_state.project_data
    brand = st.session_state.selected_brand
    brand_df = df[df["BRAND"] == brand].copy().reset_index(drop=True)

    st.markdown(f"## 🧾 Reviewing Brand: **{brand}**")
    updated_rows = []

    for i, row in brand_df.iterrows():
        with st.expander(f"FIDO: {row['FIDO']}", expanded=False):
            st.write(f"**Original Description:** {row['DESCRIPTION']}")
            st.write(f"**Original Category:** {row['CATEGORY']}")
            st.write(f"**Original Brand:** {row['BRAND']}")
            st.write(f"**Brand Status:** {row['Is Brand ID Null?']}")
            st.write(f"**GMV:** {row['GMV L365d from Data Pull Date']}")

            updated_description = st.text_area("📝 Updated Description", value=row['DESCRIPTION'], key=f"desc_{i}")
            updated_category = st.text_input("📦 Updated Category", value=row['CATEGORY'], key=f"cat_{i}")
            updated_brand = st.text_input("🏷️ Updated Brand", value=row['BRAND'], key=f"brand_{i}")
            mark_correct = st.checkbox("✅ Mark as Correct", key=f"correct_{i}")
            reviewer_notes = st.text_input("🗒️ Reviewer Notes", key=f"note_{i}")

            updated_rows.append({
                "FIDO": row["FIDO"],
                "BARCODE": row["BARCODE"],
                "Original Description": row["DESCRIPTION"],
                "Updated Description": updated_description,
                "Original Category": row["CATEGORY"],
                "Updated Category": updated_category,
                "Original Brand": row["BRAND"],
                "Updated Brand": updated_brand,
                "Is Brand ID Null?": row["Is Brand ID Null?"],
                "GMV L365d from Data Pull Date": row["GMV L365d from Data Pull Date"],
                "Mark as Correct": mark_correct,
                "Reviewer Notes": reviewer_notes
            })

    # Export section
    st.markdown("### 📤 Export Reviewed FIDOs")
    reviewed_df = pd.DataFrame(updated_rows)
    csv = reviewed_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Reviewed CSV",
        data=csv,
        file_name=f"Reviewed_{brand.replace(' ', '_')}_FIDO.csv",
        mime="text/csv"
    )

    if st.button("🔙 Back to Project List"):
        st.session_state.selected_brand = None
