"# Multi-Domain-Fraud-Detection-System" 
Fraudulent activities are rapidly increasing in areas such as online transactions, automobile insurance claims, and AI-generated content. Most existing systems are designed to detect fraud in only one domain and lack scalability and secure access mechanisms.

To address this, we developed a unified and secure web-based fraud detection system using Streamlit, capable of detecting fraud in the following three domains:

1. AI-Generated Text Detection

Implemented using a pre-trained GPT-2 model to calculate the perplexity score of input text.

Low perplexity indicates AI-generated content, while high perplexity suggests human-written text.

Example: When a paragraph was pasted, the system returned “Likely AI-Generated” based on the perplexity score.

2. Credit Card Fraud Detection

Used an Artificial Neural Network (ANN) to analyze uploaded CSV datasets of transaction records.

Each transaction was classified as fraudulent or non-fraudulent, with results shown in a color-coded table.

Example: Fraudulent rows were marked in 🔴 red, and normal ones in 🟢 green.

3. Automobile Insurance Claim Fraud Detection

Used Logistic Regression and Decision Tree models to detect fraudulent claims based on user input like vehicle type and accident location.

Example: When policy and vehicle details were entered, the system predicted and flagged suspicious claims as “Fraud.”

Additional features include:

OTP-based authentication using the Telegram API to enhance user login security.

SQLite integration for secure storage of user credentials and login data.

This project delivers real-time fraud detection with an intuitive interface, making it useful for industries like finance, insurance, and digital content verification. The modular design supports easy expansion into more fraud domains in the future.
