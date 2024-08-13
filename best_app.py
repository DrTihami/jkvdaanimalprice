
import streamlit as st
import pandas as pd
import pickle
import warnings

warnings.filterwarnings('ignore')

# Load the model and scaler
with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)
with open('scaler.pkl', 'rb') as file:
    loaded_scaler = pickle.load(file)

# Custom CSS
st.markdown("""
<style>
/* Custom styles */
body {
    background-color: #f4f4f9;
}
.main {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.stForm {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-top: 20px;
}
.stButton button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
}
.stButton button:hover {
    background-color: #0056b3;
}
.stSelectbox, .stSlider, .stTextInput {
    margin-bottom: 20px;
}
footer {
    text-align: center;
    padding: 10px;
    background-color: #f4f4f9;
}
.center-top {
    display: flex;
    justify-content: center;
    align-items: flex-start; /* Align items at the start (top) */
    margin-bottom: 20px; /* Space below the logo */
    padding-top: 20px; /* Space above the logo */
}
</style>
""", unsafe_allow_html=True)

# Main content
# Display the image
st.image('IMG-jkvda.jpg', width=150, caption='Logo')
st.markdown('<h1 class="stHeader">Animal Price Prediction Application</h1>', unsafe_allow_html=True)
st.write('This App will provide you approximate animal price based on selected parameters only')
st.markdown('<h2 class="stSubheader">Courtesy : Jammu & Kashmir Veterinary Doctors Association-Kashmir</h2>', unsafe_allow_html=True)

st.subheader('Enter the Animal details to know the Price')

# Input fields
col1, col2 = st.columns(2)
with col1:
    Animal_Breed = st.selectbox("Select the Breed of the Animal?", ("HF", "JY"))
with col2:
    Milk_Yield = st.slider("Select Milk Yield (liters)", 10, 30, value=20, step=1)

col3, col4, col5 = st.columns(3)
with col3:
    Parity_No = st.selectbox("Select Lactation No of Animal?", [0, 1, 2, 3])
with col4:
    Pregnancy_Status = st.selectbox("Select Pregnancy Status?", ("Yes", "No"))
# Conditionally set Pregnancy_Trimester
with col5:
    if Pregnancy_Status == "No":
        Pregnancy_Trimester = 0
    else:
        Pregnancy_Trimester = st.selectbox("Select Pregnancy Trimester?", [1, 2, 3])

# Map Yes/No to 1/0
Animal_Breed = 1 if Animal_Breed == 'JY' else 0
Pregnancy_Status = 1 if Pregnancy_Status == 'Yes' else 0

# Prepare the input data for prediction
input_data = {
    'Animal_Breed': [Animal_Breed],
    'Milk_Yield': [Milk_Yield],
    'Parity_No': [Parity_No],
    'Pregnancy_Status': [Pregnancy_Status],
    'Pregnancy_Trimester': [Pregnancy_Trimester]
}

# Convert input data to dataframe
input_df = pd.DataFrame(input_data)

# Scale the input data
scaled_df = loaded_scaler.transform(input_df)

# Make prediction
if st.button('Predict Animal Price'):
    predicted_price = loaded_model.predict(scaled_df)
    Animal_Price = round(predicted_price[0])
    st.write(f'The Price of selected Dairy Animal is Rupees : {Animal_Price}')

# Footer
st.markdown("""
<footer>
    <p style='font-size: 18px;'> <a href='https://yourwebsite.com'>jkvda.org</a></p>
</footer>
""", unsafe_allow_html=True)