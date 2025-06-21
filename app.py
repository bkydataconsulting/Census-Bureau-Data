import streamlit as st
# Import the new function for income metrics by ZIP code
from get_data import get_median_income_by_zip
import pandas as pd

# Update the title and description to reflect ZIP code level income metrics
st.title("US Census Median Household Income by ZIP Code")
st.markdown("Displays median household income and population by U.S. ZIP code (ZCTA) using 2022 ACS 5-Year Estimates.")

try:
    # Use the new function to get income and population data by ZIP code
    df = get_median_income_by_zip()

    # --- Add state filter ---
    states = df["State_Name"].dropna().unique()
    selected_state = st.selectbox("Select a state:", ["All"] + sorted(states))
    if selected_state != "All":
        df = df[df["State_Name"] == selected_state]
    # ---

    st.dataframe(df, use_container_width=True)

    # Show a bar chart of median income by ZIP code (showing top 20 for readability)
    st.bar_chart(df.set_index("ZIP_Code")["Median_Income"].head(20))
except Exception as e:
    st.error(f"Error fetching data: {e}")