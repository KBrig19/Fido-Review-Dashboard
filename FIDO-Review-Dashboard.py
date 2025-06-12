# Rewriting the updated brand review loop with individual no-change options for description, category, and brand
updated_code = """
# --- Brand Review Page ---
if st.session_state.page == "brand_review":
    df = st.session_state.project_data
    brand = st.session_state.selected_brand
    brand_df = df[df["BRAND"] == brand].copy().reset_index(drop=True)

    st.markdown(f"<div class='sticky-header'><h2> Reviewing Brand: {brand}</h2></div>", unsafe_allow_html=True)

    # Sidebar controls
    with st.sidebar:
        st.markdown("### 🛠️ Controls")
        if st.button("💾 Save All"):
            for i, row in brand_df.iterrows():
                fido = row["FIDO"]
                st.session_state.saved_reviews[fido] = {
                    "FIDO": fido,
                    "BARCODE": row["BARCODE"],
                    "Original Description": row["DESCRIPTION"],
                    "Updated Description": st.session_state.get(f"desc_{i}", row["DESCRIPTION"]) if not st.session_state.get(f"desc_nc_{i}") else row["DESCRIPTION"],
                    "Original Category": row["CATEGORY"],
                    "Updated Category": st.session_state.get(f"cat_{i}", row["CATEGORY"]) if not st.session_state.get(f"cat_nc_{i}") else row["CATEGORY"],
                    "Original Brand": row["BRAND"],
                    "Updated Brand": st.session_state.get(f"brand_{i}", row["BRAND"]) if not st.session_state.get(f"brand_nc_{i}") else row["BRAND"],
                    "BRAND_ID": row.get("BRAND_ID", ""),
                    "Is Brand ID Null?": row["Is Brand ID Null?"],
                    "GMV L365d from Data Pull Date": row["GMV L365d from Data Pull Date"],
                    "Reviewer Notes": st.session_state.get(f"note_{i}", ""),
                    "No Change - Description": st.session_state.get(f"desc_nc_{i}", False),
                    "No Change - Category": st.session_state.get(f"cat_nc_{i}", False),
                    "No Change - Brand": st.session_state.get(f"brand_nc_{i}", False)
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

        # Inputs for updates + individual 'no change' toggles
        st.markdown("**✏️ Make Updates or Mark No Change Individually**")

        no_change_desc = st.checkbox("📝 No Change to Description", key=f"desc_nc_{i}")
        updated_desc = row["DESCRIPTION"] if no_change_desc else st.text_area("Updated Description", value=row["DESCRIPTION"], key=f"desc_{i}")

        no_change_cat = st.checkbox("📦 No Change to Category", key=f"cat_nc_{i}")
        updated_cat = row["CATEGORY"] if no_change_cat else st.text_input("Updated Category", value=row["CATEGORY"], key=f"cat_{i}")

        no_change_brand = st.checkbox("🏷️ No Change to Brand", key=f"brand_nc_{i}")
        updated_brand = row["BRAND"] if no_change_brand else st.text_input("Updated Brand", value=row["BRAND"], key=f"brand_{i}")

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
                "Reviewer Notes": reviewer_note,
                "No Change - Description": no_change_desc,
                "No Change - Category": no_change_cat,
                "No Change - Brand": no_change_brand
            }
            st.success(f"✅ Saved {row['FIDO']}")
"""
