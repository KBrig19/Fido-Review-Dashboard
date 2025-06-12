# Append the remaining logic to the optimized Streamlit app file
additional_code = """
# --- Brand Review Page ---
if st.session_state.page == "brand_review":
    df = st.session_state.project_data
    brand = st.session_state.selected_brand
    brand_df = df[df["BRAND"] == brand].copy().reset_index(drop=True)

    st.markdown(f"<div class='sticky-header'><h2>🧾 Reviewing Brand: {brand}</h2></div>", unsafe_allow_html=True)

    st.sidebar.header("View Options")
    view_choice = st.sidebar.radio("Select View Mode:", ["Fast View", "Full View"])
    st.session_state.view_mode = view_choice

    total_pages = (len(brand_df) - 1) // FIDOS_PER_PAGE + 1
    start_idx = st.session_state.page_number * FIDOS_PER_PAGE
    end_idx = start_idx + FIDOS_PER_PAGE
    paginated_df = brand_df.iloc[start_idx:end_idx]

    st.sidebar.markdown("### Page Navigation")
    if st.sidebar.button("⬅️ Previous") and st.session_state.page_number > 0:
        st.session_state.page_number -= 1
    if st.sidebar.button("➡️ Next") and st.session_state.page_number < total_pages - 1:
        st.session_state.page_number += 1
    st.sidebar.markdown(f"Page {st.session_state.page_number + 1} of {total_pages}")

    with st.sidebar:
        if st.button("💾 Save All (This Page)"):
            for i, row in paginated_df.iterrows():
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
                    "Reviewer Notes": st.session_state.get(f"note_{i}", ""),
                    "Reviewed By": st.session_state.reviewer_name,
                    "Review Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

    for i, row in paginated_df.iterrows():
        show_block = (st.session_state.view_mode == "Full View") or st.expander(f"FIDO: {row['FIDO']}", expanded=False)
        if st.session_state.view_mode == "Full View" or show_block:
            st.subheader(f"FIDO: {row['F