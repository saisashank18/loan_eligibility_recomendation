import streamlit as st
import pandas as pd
import SessionState
import pandas as pd
import pickle

s = SessionState.get(button=False, button2=False)
#s2 = SessionState.get(button2=False)

def Recommender(Loan_Amount):
    st.title("Congratulations!! Your are Eligible")
    data = pd.read_csv('data.csv')
    data.drop(['Turnaround Time'],axis=1,inplace=True)
    data.drop(['Processing Fee'],axis=1,inplace=True)
    data = data[data['Minimum Loan Amount'] <= Loan_Amount]
    data = data[data['Maximum Loan Amount'] >= Loan_Amount]
    data = data.sort_values(['Minimum Interest rate','Maximum Interest rate'], ascending=True)
    # resetting index
    data.reset_index(inplace = True)
    data.drop(['index'],axis=1,inplace=True)
    print(data)
    st.table(data.head(7))

def MLmodel(gender, married, self_employed, Dependents, Applicant_Income, Co_Applicant_Income, Loan_Amount, Loan_Amount_term, Property_area, Credit_History, education):
    data = [{'Gender': gender, 'Married': married, 'Dependents': Dependents, 'Education': education, 'Self_Employed': self_employed, 'ApplicantIncome': Applicant_Income,
             'CoapplicantIncome': Co_Applicant_Income, 'LoanAmount': Loan_Amount, 'Loan_Amount_Term': Loan_Amount_term, 'Credit_History': Credit_History, 'Property_Area': Property_area}]
    df = pd.DataFrame(data)
    df.Gender.replace(('Male', 'Female'), (1, 0), inplace=True)
    df.Dependents.replace(('0', '1', '2', '3+'),
                          (0, 0.25, 0.5, 1), inplace=True)
    df.Married.replace(('Yes', 'No'), (1, 0), inplace=True)
    df.Education.replace(('Graduate', 'Not Graduate'), (1, 0), inplace=True)
    df.Self_Employed.replace(('No', 'Yes'), (1, 0), inplace=True)
    df.Property_Area.replace(
        ('Urban', 'Semiurban',  'Rural'), (1, 0.5, 0), inplace=True)
    filename = 'model3.sav'
    model = pickle.load(open(filename, 'rb'))
    res = model.predict(df)
    res = res.tolist()
    print(res[0])
    result = res[0]
    term = Loan_Amount_term * 4
    if(term < 360):
        st.write("Not Eligible")
    elif(Loan_Amount < Applicant_Income):
        #st.write("Eligible")
        Recommender(Loan_Amount)
    elif(Applicant_Income < 30000 and Loan_Amount > 500000):
        st.write("Not Eligible")
    elif(education == 'Not Graduate' and Applicant_Income < 30000):
        st.write("Not Eligible")
    elif(Loan_Amount > 500000 and term < 1000):
        st.write("Not Eligible")
    # elif(Loan_Amount == 4 * Applicant_Income):
    #     st.write("Not Eligible")
    elif(Credit_History == 0 and Applicant_Income < 100000):
        st.write("Not Eligible")
    elif(Property_area == 'Rural' and Applicant_Income < 50000):
        st.write("Not Eligible")
    elif(Dependents == '3+' and Applicant_Income < 70000):
        st.write("Not Eligible")
    elif(Property_area == 'Semiurban' and education == 'Not Garduate' and Applicant_Income < 80000):
        st.write("Not Eligible")
    elif(Loan_Amount < 10000 and Loan_Amount > 3000000):
        st.write("Not Eligible, Your Loan Amount is either too High or too Low")
    elif(res[0] == 1):
        #st.write("Eligible")
        Recommender(Loan_Amount)
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
    gender = st.selectbox('Gender', ('Male', 'Female'))
    married = st.selectbox('Are You Married?', ('Yes', 'No'))
    education = st.selectbox('Select your Education',
                             ('Graduate', 'Not Graduate'))
    self_employed = st.selectbox('Are You Self Employed?', ('Yes', 'No'))
    Dependents = st.selectbox(
        'How many Dependents do you have?', ('0', '1', '2', '3+'))
    Applicant_Income = st.number_input("Applicant Income (In Month)", 0)
    Co_Applicant_Income = st.number_input(
        "Co-Applicant Income (If no Co-Applicant enter Zero)", 0)
    Loan_Amount = st.number_input("Please enter your Loan Amount", 0)
    Loan_Amount_term = st.number_input(
        "Please enter your Loan Amount term in days", 0)
    Property_area = st.selectbox(
        'Please select your Area', ('Urban', 'Semiurban', 'Rural'))
    Credit_History = st.selectbox(
        'Have you cleared your Credit History', ('Yes', 'No'))
    if Credit_History == 'Yes':
        Credit_History = 1
    else:
        Credit_History = 0

    if st.button("Run Model") or s.button2:
        s.button2 = True
        # st.write(gender," ",married," ",self_employed," ",Applicant_Income," ",Co_Applicant_Income," ",Loan_Amount,
        #    " ",Loan_Amount_term," ",Property_area," ",Credit_History," ")
        # run model
        MLmodel(gender, married, self_employed, Dependents, Applicant_Income,
                Co_Applicant_Income, Loan_Amount, Loan_Amount_term/4, Property_area, Credit_History, education)


def basicEligibility(name, age, cibil):
    age = int(age)
    cibil = int(cibil)
    if(cibil < 300 or cibil > 900):
        st.write("Enter valid CIBIL Score")
        return
    elif age > 18 and cibil >= 700:
        preprocessML()
        return
    elif(cibil < 700):
        st.write("Not Eligible, You don't have good CIBIL Score, Minimum is 700")
        return
    elif(age < 18):
        st.write("Your have to be above 18 to apply for a loan")
        return
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
