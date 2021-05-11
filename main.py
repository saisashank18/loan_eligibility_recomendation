import webbrowser
from altair.vegalite.v4.api import _dataset_name
import streamlit as st
import pandas as pd
from sklearn import datasets
st.title("Optimal loan predictor")

user_input_1 = st.text_input("Name", )
user_input_2 = st.text_input("Age", )
user_input_3 = st.text_input("CIBIL Score", )


def preprocess(name, age, cibil):
    if(type(name) == str):
        try:
            age = int(age)
            cibil = int(cibil)
            basicEligibility(name, age, cibil)
        except ValueError:
            st.write("Invalid Input")
    else:
        st.write("Invalid Input")


def basicEligibility(name, age, cibil):
    if int(age) > 18:
        st.text_input("hello", )
        st.write("Your Details: ", name, ",",
                 age, ",", cibil,)
        # ML Model function calling
    else:
        st.write("Not Eligible")
    return


if st.button("Submit"):
    preprocess(user_input_1, user_input_2, user_input_3)


url = 'https://www.streamlit.io/'

if st.button('Open browser'):
    # webbrowser.open_new_tab(url)
    webbrowser.open(url, new=1)

st.sidebar.title("settings")
