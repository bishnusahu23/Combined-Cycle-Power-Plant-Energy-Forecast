#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

# App title and description
st.markdown("""<h2 style='text-align:left;color:YellowGreen;'>Combined Cycle Power Plant - Energy production prediction</h2>""", unsafe_allow_html=True)

st.markdown("""
This app predicts the energy production of a combined cycle power plant based on several environmental factors.
Please enter the required values to get the prediction.
""")

# User inputs with some initial default values for better user experience
temp = st.number_input("Ambient Temperature (°C):", value=9.59)
pressure = st.number_input("Ambient Pressure (Millibar):", value=1017.01)
humidity = st.number_input("Relative Humidity (%):", value=60.10)
vacuum = st.number_input("Exhaust Vacuum (cm Hg):", value=38.56)


try:
    with open(r"Regression_model", 'rb') as file:
        model = pickle.load(file)
    # importing the scaler to transform the new data
    with open(r"scaler.pkl", 'rb') as file:
        scaler = pickle.load(file)
    # loading the dataset
    data = pd.read_csv(r"Copy of energy_production .csv")
    
except FileNotFoundError as e:
    st.error(f"File not found: {e}. Please check the file path and try again.")
    st.stop()

# Create a DataFrame with user input
input_data = pd.DataFrame({
    'temperature': [temp],
    'exhaust_vacuum': [vacuum],
    'amb_pressure': [pressure],
    'r_humidity': [humidity]
})

scaled_input_data = scaler.transform(input_data)

# Button to trigger prediction
if st.button("Predict"):
    # Predict and display result
    try:
        predictions = model.predict(scaled_input_data)

        # Get mean and standard deviation for energy production
        mean_energy = data['energy_production'].mean()
        std_energy = data['energy_production'].std()
        
         # Inverse standardization
        original_predictions = predictions * std_energy + mean_energy
        
        # Display prediction result
        st.success(f"Predicted Energy Production: {original_predictions[0]:.2f} MW")
    except Exception as e:
        st.error(f"Error in prediction: {e}")
