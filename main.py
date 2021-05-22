import streamlit as st
import pandas as pd
import SessionState
import pandas as pd
import pickle

s = SessionState.get(button=False,button2=False)
#s2 = SessionState.get(button2=False)

def MLmodel(gender,married,self_employed,Dependents,Applicant_Income,Co_Applicant_Income,Loan_Amount,Loan_Amount_term,Property_area,Credit_History,education):
    data = [{'Gender': gender, 'Married': married, 'Dependents':Dependents, 'Education': education, 'Self_Employed': self_employed, 'ApplicantIncome':Applicant_Income,'CoapplicantIncome': Co_Applicant_Income, 'LoanAmount': Loan_Amount, 'Loan_Amount_Term':Loan_Amount_term,'Credit_History': Credit_History, 'Property_Area': Property_area}]
    df = pd.DataFrame(data)
    df.Gender.replace(('Male', 'Female'), (1, 0), inplace=True)
    df.Dependents.replace(('0', '1', '2', '3+'), (0, 0.25, 0.5, 1), inplace=True)
    df.Married.replace(('Yes', 'No'), (1, 0), inplace=True)
    df.Education.replace(('Graduate', 'Not Graduate'), (1, 0), inplace=True)
    df.Self_Employed.replace(('No', 'Yes'), (1, 0), inplace=True)
    df.Property_Area.replace(('Urban', 'Semiurban',  'Rural'), (1, 0.5, 0), inplace=True)
    filename = 'model3.sav'
    model = pickle.load(open(filename, 'rb'))
    res = model.predict(df)
    res = res.tolist()
    print(res[0])
    
    
    
    
    if(res[0]==1):
        st.write("Eligible")
    else:
        st.write("Not Eligible")


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
    education = st.selectbox('Select your Education',('Graduate', 'Not Graduate'))
    self_employed = st.selectbox('Are You Self Employed?',('Yes', 'No'))
    Dependents = st.selectbox('How many Dependents do you have?',('0','1', '2','3+'))
    Applicant_Income = st.number_input("Applicant Income (In Month)", 0)
    Co_Applicant_Income = st.number_input("Co-Applicant Income (If no Co-Applicant enter Zero)", 0)
    Loan_Amount = st.number_input("Please enter your Loan Amount", 0)
    Loan_Amount_term = st.number_input("Please enter your Loan Amount term in days", 0)
    Property_area = st.selectbox('Please select your Area',('Urban', 'Semiurban','Rural'))
    Credit_History = st.selectbox('Have you cleared your Credit History',('Yes', 'No'))
    if Credit_History=='Yes':
        Credit_History=1
    else:
        Credit_History=0
    
    if st.button("Run Model") or s.button2:
        s.button2 = True
        #st.write(gender," ",married," ",self_employed," ",Applicant_Income," ",Co_Applicant_Income," ",Loan_Amount,
        #    " ",Loan_Amount_term," ",Property_area," ",Credit_History," ")
        #run model
        MLmodel(gender,married,self_employed,Dependents,Applicant_Income,
            Co_Applicant_Income,Loan_Amount,Loan_Amount_term,Property_area,Credit_History,education)


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
    if st.button("Check Basic Eligibility") or s.button:
        s.button = True
        preprocess(user_input_1, user_input_2, user_input_3)

if __name__ == '__main__':
	main()