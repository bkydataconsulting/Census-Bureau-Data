import streamlit as st
# Import the new function for income metrics by ZIP code
from get_data import get_median_income_by_zip
import pandas as pd
import pydeck as pdk

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

    # Always sort by Median_Income descending before showing
    df = df.sort_values(by="Median_Income", ascending=False)

    st.dataframe(df, use_container_width=True)

    # Show a map of the top 500 ZIP codes by median income, dot size by income
    top500 = df.head(500).copy()
    top500 = top500.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    min_income = top500["Median_Income"].min()
    max_income = top500["Median_Income"].max()
    if max_income == min_income:
        top500["radius"] = 1000
    else:
        top500["radius"] = 1000 + 4000 * (top500["Median_Income"] - min_income) / (max_income - min_income)
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=top500,
        get_position='[lon, lat]',
        get_radius="radius",
        get_fill_color=[255, 0, 0, 140],
        pickable=True,
        auto_highlight=True,
    )
    view_state = pdk.ViewState(
        latitude=top500["lat"].mean(),
        longitude=top500["lon"].mean(),
        zoom=4,
        pitch=0,
    )
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "ZIP: {ZIP_Code}\nIncome: ${Median_Income}"}))
except Exception as e:
    st.error(f"Error fetching data: {e}")