import webbrowser
from altair.vegalite.v4.api import _dataset_name
import streamlit as st
import pandas as pd
from sklearn import datasets
import st_state_patch as st_state
import SessionState

s = SessionState.get(button=False)

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

def preprocessML():
    gender = st.selectbox('Gender',('Male', 'Female'))
    married = st.selectbox('Are You Married?',('Yes', 'No'))
    self_employed = st.selectbox('Are You Self Employed?',('Yes', 'No'))
    Applicant_Income = st.number_input("Applicant Income", )
    Co_Applicant_Income = st.number_input("Co-Applicant Income (If no Co-Applicant enter Zero)", )
    Loan_Amount = st.number_input("Please enter your Loan Amount", )
    Loan_Amount_term = st.number_input("Please enter your Loan Amount term in days", )
    Property_area = st.selectbox('Please select your Area',('Urban', 'Semiurban','Rural'))
    Credit_History = st.selectbox('Do you have Credit History',('Yes', 'No'))
    if Credit_History=='Yes':
        Credit_History=1
    else:
        Credit_History=0
    
    st.write(gender," ",married," ",self_employed," ",Applicant_Income," ",Co_Applicant_Income," ",Loan_Amount,
        " ",Loan_Amount_term," ",Property_area," ",Credit_History," ")

def basicEligibility(name, age, cibil):
    if int(age) > 18:
        preprocessML()
    else:
        st.write("Not Eligible")
    return



def main():
    st.title("Optimal loan predictor")
    user_input_1 = st.text_input("Name", )
    user_input_2 = st.text_input("Age", )
    user_input_3 = st.text_input("CIBIL Score", )
    if st.button("Submit") or s.button:
        s.button = True
        preprocess(user_input_1, user_input_2, user_input_3)

if __name__ == '__main__':
	main()