
import streamlit as st
import scikitlearn
import pandas as pd
import pickle
import warnings

warnings.filterwarnings('ignore')

# Load the model
with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Load the Scaler
with open('scaler.pkl', 'rb') as file:
    loaded_scaler = pickle.load(file)

# Inject custom CSS for font size adjustments and alignment
st.markdown("""
<style>
/* Font size for buttons */
.stButton button {
    font-size: 18px; /* Adjust the font size for buttons */
}

/* Font size for sliders */
.stSlider > div > div > input {
    font-size: 18px; /* Adjust the font size for slider inputs */
}

/* Font size for select boxes */
.stSelectbox div[data-baseweb="select"] {
    font-size: 18px; /* Adjust the font size for select boxes */
}

/* Font size for text input */
.stTextInput input {
    font-size: 18px; /* Adjust the font size for text input fields */
}

/* Font size for output text (such as prediction result) */
.stWrite {
    font-size: 22px; /* Adjust the font size for output text */
}

/* Font size for labels above select boxes and sliders */
.stMarkdown p {
    font-size: 20px; /* Adjust the font size for labels */
}

/* Center align headers and subheaders */
.stHeader, .stSubheader {
    text-align: center; /* Center align the text */
}

/* Optional: adjust the header and subheader sizes */
.stHeader {
    font-size: 36px; /* Adjust the font size for the header */
}

.stSubheader {
    font-size: 28px; /* Adjust the font size for the subheader */
}
</style>
""", unsafe_allow_html=True)

# Headings and creator name
st.markdown('<h1 class="stHeader">Animal Price Prediction Application</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="stSubheader">Courtesy : Jammu & Kashmir Veterinary Doctors Association-Kashmir</h2>', unsafe_allow_html=True)

st.subheader('Enter the Animal details to know the Price')

# Input fields
col1, col2 = st.columns(2)
with col1:
    Animal_Breed = st.selectbox("Select the Breed of the Animal?", ("HF", "JY"))
with col2:
    Milk_Yield = st.slider("Select Milk Yield", 10, 30)

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
if st.button('Predict Premium Price'):
    predicted_price = loaded_model.predict(scaled_df)
    Animal_Price = round(predicted_price[0])
    st.write(f'The Price of selected Dairy Animal is Rupees : {Animal_Price}')
