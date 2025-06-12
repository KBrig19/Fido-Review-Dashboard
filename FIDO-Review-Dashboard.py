import streamlit as st
import pandas as pd

st.set_page_config(page_title="FIDO Review Dashboard", layout="wide")
st.title("🧾 FIDO Review Dashboard – Manual Verification Tool")

uploaded_file = st.file_uploader("Upload your FIDO Review CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Prepare lists for dropdowns
    category_options = sorted(df["CATEGORY"].dropna().unique().tolist())
    brand_options = sorted(df["BRAND"].dropna().unique().tolist())

    st.sidebar.header("🔍 Filter Options")
    brand_filter = st.sidebar.multiselect("Filter by Brand", brand_options)
    category_filter = st.sidebar.multiselect("Filter by Category", category_options)

    filtered_df = df.copy()
    if brand_filter:
        filtered_df = filtered_df[filtered_df["BRAND"].isin(brand_filter)]
    if category_filter:
        filtered_df = filtered_df[filtered_df["CATEGORY"].isin(category_filter)]

    st.markdown("### 🧾 FIDOs Ready for Review")
    updated_rows = []

    for i, row in filtered_df.iterrows():
        with st.expander(f"FIDO: {row['FIDO']}"):
            st.write(f"**Original Description:** {row['DESCRIPTION']}")
            st.write(f"**Original Category:** {row['CATEGORY']}")
            st.write(f"**Original Brand:** {row['BRAND']}")
            st.write(f"**Brand Assignment Status:** {row['Is Brand ID Null?']}")
            st.write(f"**GMV (Last 365 Days):** {row['GMV L365d from Data Pull Date']}")

            # Reviewer inputs
            is_verified = st.checkbox("✅ Mark as Correct", key=f"correct_{i}")
            updated_desc = st.text_area("📝 Updated Description", value=row["DESCRIPTION"], key=f"desc_{i}")
            updated_cat = st.selectbox("📦 Updated Category", options=category_options + ["Other"], index=category_options.index(row["CATEGORY"]) if pd.notna(row["CATEGORY"]) and row["CATEGORY"] in category_options else 0, key=f"cat_{i}")
            updated_brand = st.selectbox("🏷️ Updated Brand", options=brand_options + ["Other"], index=brand_options.index(row["BRAND"]) if pd.notna(row["BRAND"]) and row["BRAND"] in brand_options else 0, key=f"brand_{i}")
            reviewer_note = st.text_input("🗒️ Notes", key=f"note_{i}")

            updated_rows.append({
                "FIDO": row["FIDO"],
                "Original Description": row["DESCRIPTION"],
                "Updated Description": updated_desc,
                "Original Category": row["CATEGORY"],
                "Updated Category": updated_cat,
                "Original Brand": row["BRAND"],
                "Updated Brand": updated_brand,
                "Is Brand ID Null?": row["Is Brand ID Null?"],
                "GMV L365d from Data Pull Date": row["GMV L365d from Data Pull Date"],
                "Mark as Correct": is_verified,
                "Reviewer Notes": reviewer_note
            })

    if updated_rows:
        st.markdown("### 📤 Export Your Reviewed FIDOs")
        reviewed_df = pd.DataFrame(updated_rows)
        csv = reviewed_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv, file_name="reviewed_fidos.csv", mime="text/csv")
