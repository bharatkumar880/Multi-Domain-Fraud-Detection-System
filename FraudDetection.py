import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
from Essay_fraud import PerplexityApp


class FraudDetectionApp:
    def __init__(self):
        self.model_choice = None
        self.credit_card_model = None
        self.fraud_model = None
        self.label_encoders = None

    def load_credit_card_model(self):
        if not self.credit_card_model:
            self.credit_card_model = joblib.load(r"C:\Users\HP\Downloads\FraudFortify\FraudFortify\Model\ann_model.pkl")
        return self.credit_card_model

    def load_fraud_model(self):
        if not self.fraud_model:
            with open(r'C:\Users\HP\Downloads\FraudFortify\FraudFortify\Model\fraud_detection_model.pkl', 'rb') as model_file:
                self.fraud_model = pickle.load(model_file)
            with open(r'C:\Users\HP\Downloads\FraudFortify\FraudFortify\Model\label_encoders.pkl', 'rb') as encoders_file:
                self.label_encoders = pickle.load(encoders_file)
        return self.fraud_model, self.label_encoders

    def run(self):
        # Add a sidebar image
        st.sidebar.image("Images/main.png", use_container_width=True)

        # Add a brief summary of the application
        st.sidebar.markdown("""
            ## Welcome to the Multi-Domain Fraud Detection System
            This application offers:
            - **Credit Card Fraud Detection**: Identify fraudulent transactions with high accuracy.
            - **General Fraud Detection**: Detect fraudulent insurance claims using machine learning.
            - **GPT-Generated Text Detection**: Determine if a text is AI-generated using perplexity analysis.
        """)

        # Model selection
        st.sidebar.title("Choose a Model")
        self.model_choice = st.sidebar.radio(
            "Select the type of fraud detection:",
            ["Credit Card Fraud Detection", "Insurance Fraud Detection", "Detect GPT Generated Text"]
        )

        # Show additional information based on the selection
        if self.model_choice == "Credit Card Fraud Detection":
            st.sidebar.image(r"C:\Users\HP\Downloads\FraudFortify\FraudFortify\Images\card.png", use_container_width=True)
            st.sidebar.markdown("""
                ### Credit Card Fraud Detection
                - Upload transaction data.
                - Predict fraudulent transactions with our trained ANN model.
            """)
            self.credit_card_fraud_detection()
        elif self.model_choice == "Insurance Fraud Detection":
            st.sidebar.image(r"C:\Users\HP\Downloads\FraudFortify\FraudFortify\Images\car.png", use_container_width=True)
            st.sidebar.markdown("""
                ### General Fraud Detection
                - Input claim details.
                - Predict fraudulent insurance claims using supervised learning.
            """)
            self.general_fraud_detection()
        elif self.model_choice == "Detect GPT Generated Text":
            st.sidebar.image(r"C:\Users\HP\Downloads\FraudFortify\FraudFortify\Images\chat.png", use_container_width=True)
            st.sidebar.markdown("""
                ### Detect GPT-Generated Text
                - Paste text or upload a file.
                - Analyze perplexity to identify AI-generated content.
            """)
            PerplexityApp()

    def credit_card_fraud_detection(self):
        st.title("Credit Card Fraud Detection")
        st.write("Upload a CSV file with test data to predict fraud cases.")
        credit_card_model = self.load_credit_card_model()

        uploaded_file = st.file_uploader("Upload your test data (CSV format)", type=["csv"])
        if uploaded_file:
            X_test_df = pd.read_csv(uploaded_file)
            st.write("Test data preview:")
            st.dataframe(X_test_df.head())

            y_pred = credit_card_model.predict(X_test_df)
            predicted_labels = ['Credit Card Fraud Detected' if pred == 1 else 'Normal' for pred in y_pred]

            predict_df = X_test_df.copy()
            predict_df['Predicted_Class'] = predicted_labels

            st.write("Predictions:")
            st.dataframe(predict_df.head(2000))

            fraud_detected = predict_df[predict_df['Predicted_Class'] == 'Credit Card Fraud Detected']
            st.write("Top 10 'Credit Card Fraud Detected' instances:")
            st.dataframe(fraud_detected.head(10))

            csv = predict_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Predictions as CSV",
                data=csv,
                file_name='predicted_results.csv',
                mime='text/csv',
            )

    def general_fraud_detection(self):
        st.title("Fraud Detection Prediction")
        st.write("Input details to predict fraud.")
        fraud_model, label_encoders = self.load_fraud_model()

        def get_user_input():
            BasePolicy = st.selectbox("BasePolicy", label_encoders['BasePolicy'].classes_)
            Fault = st.selectbox("Fault", label_encoders['Fault'].classes_)
            VehicleCategory = st.selectbox("VehicleCategory", label_encoders['VehicleCategory'].classes_)
            VehiclePrice = st.selectbox("VehiclePrice", label_encoders['VehiclePrice'].classes_)
            PolicyType = st.selectbox("PolicyType", label_encoders['PolicyType'].classes_)
            Sex = st.selectbox("Sex", label_encoders['Sex'].classes_)
            AddressChange_Claim = st.selectbox("AddressChange_Claim", label_encoders['AddressChange_Claim'].classes_)
            AccidentArea = st.selectbox("AccidentArea", label_encoders['AccidentArea'].classes_)
            AgeOfPolicyHolder = st.selectbox("AgeOfPolicyHolder", label_encoders['AgeOfPolicyHolder'].classes_)
            Age = st.number_input("Age", min_value=0, max_value=120, value=25)

            features = {
                'BasePolicy': label_encoders['BasePolicy'].transform([BasePolicy])[0],
                'Fault': label_encoders['Fault'].transform([Fault])[0],
                'VehicleCategory': label_encoders['VehicleCategory'].transform([VehicleCategory])[0],
                'VehiclePrice': label_encoders['VehiclePrice'].transform([VehiclePrice])[0],
                'PolicyType': label_encoders['PolicyType'].transform([PolicyType])[0],
                'Sex': label_encoders['Sex'].transform([Sex])[0],
                'AddressChange_Claim': label_encoders['AddressChange_Claim'].transform([AddressChange_Claim])[0],
                'AccidentArea': label_encoders['AccidentArea'].transform([AccidentArea])[0],
                'AgeOfPolicyHolder': label_encoders['AgeOfPolicyHolder'].transform([AgeOfPolicyHolder])[0],
                'Age': Age
            }
            return np.array(list(features.values())).reshape(1, -1)

        input_data = get_user_input()

        if st.button("Predict"):
            prediction = fraud_model.predict(input_data)[0]
            if prediction == 1:
                st.markdown("<h1 style='color: red;'>Fraud Detected</h1>", unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='color: green;'>No Fraud</h1>", unsafe_allow_html=True)


# Instantiate and run the application
if __name__ == "__main__":
    app = FraudDetectionApp()
    app.run()
