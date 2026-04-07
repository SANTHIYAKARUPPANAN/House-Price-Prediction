import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model
model = joblib.load("house_price_model.pkl")

# ---------- UI ----------
st.title("🏠 House Price Prediction App")
st.markdown("Predict house prices using machine learning based on key features.")

st.markdown("### 📝 Enter House Details")

# Layout (2 columns)
col1, col2 = st.columns(2)

with col1:
    qual = st.slider("Overall Quality (1-10)", 1, 10)
    tot_rooms = st.number_input("Total Rooms", min_value=1)
    year_built = st.number_input("Year Built", min_value=1900, max_value=2025)

with col2:
    Garage_option = st.selectbox("Garage Available?", ["Yes", "No"])
    Garage = 1 if Garage_option == "Yes" else 0

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

    area = st.number_input("Total Area (sqft)", min_value=1)
    area = np.log1p(area)

# ---------- Prediction ----------
def predict_price():
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

# ---------- Button ----------
if st.button("💰 Predict Price"):
    price = predict_price()
    st.success(f"Estimated House Price: ₹ {round(price,2)}")
    if price < 2000000:
        st.info("This is a low-priced property.")
    elif price < 5000000:
        st.info("This is a mid-range property.")
    else:
        st.info("This is a high-value property.")

# ---------- Extra Info ----------
st.markdown("---")
st.markdown("### 📊 Model Information")
st.write("""
- Model: Machine Learning Regression Model  
- Features: Area, Rooms, Quality, Year Built, Garage Details  
- Output: Estimated House Price  
""")
