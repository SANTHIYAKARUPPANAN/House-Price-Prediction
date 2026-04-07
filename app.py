import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model
model = joblib.load("house_price_model.pkl")

# Title
st.title("🏠 House Price Prediction App")

st.markdown("### Enter house details below:")

# Inputs
qual = st.slider("Overall Quality", 1, 10)
tot_rooms = st.number_input("Total Rooms", min_value=1)
year_built = st.number_input("Year Built", min_value=1900, max_value=2025)

Garage = st.selectbox("Garage Available?", [1, 0])

garage_yr = 0
nogarage = 0
rough_finish = 0
unfinish = 0

if Garage == 1:
    garage_yr = st.number_input("Garage Year Built", min_value=1900, max_value=2025)
    Garage_cond = st.selectbox("Garage Finish", ["Rough", "Unfinished"])

    if Garage_cond == "Rough":
        rough_finish = 1
    else:
        unfinish = 1
else:
    nogarage = 1

area = st.number_input("Total Area (sqft)")
area = np.log1p(area)

# Prediction function
def house_price_prediction():
    input_data = pd.DataFrame({
        "Overall Qual": [qual],
        "Garage Yr Blt": [garage_yr],
        "TotRms AbvGrd": [tot_rooms],
        "Year Built": [year_built],
        "Garage": [Garage],
        "Total SF Area": [area],
        "Garage Finish_NoGarage": [nogarage],
        "Garage Finish_RFn": [rough_finish],
        "Garage Finish_Unf": [unfinish]
    })

    prediction = model.predict(input_data)
    prediction = np.expm1(prediction)
    return prediction[0]

# Button
if st.button("Predict Price"):
    price = house_price_prediction()
    st.success(f"Predicted House Price: ₹ {round(price,2)}")
