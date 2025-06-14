import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load the dataset
data = pd.read_csv(r"C:\Users\HP\Downloads\FraudFortify\FraudFortify\Dataset\fraud_oracle_balanced_top10_original.csv")

# Encode categorical variables
categorical_columns = [
    'BasePolicy', 'Fault', 'VehicleCategory', 'VehiclePrice', 'PolicyType',
    'Sex', 'AddressChange_Claim', 'AccidentArea', 'AgeOfPolicyHolder'
]

label_encoders = {col: LabelEncoder() for col in categorical_columns}
for col in categorical_columns:
    data[col] = label_encoders[col].fit_transform(data[col])

# Split data into features and target
X = data.drop(columns=['FraudFound_P'])
y = data['FraudFound_P']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the model and label encoders
with open(r"C:\Users\HP\Downloads\FraudFortify\FraudFortify\Model\fraud_detection_model.pkl", 'wb') as model_file:
    pickle.dump(model, model_file)

with open(r"C:\Users\HP\Downloads\FraudFortify\FraudFortify\Model\label_encoders.pkl", 'wb') as encoders_file:
    pickle.dump(label_encoders, encoders_file)

print("Model and encoders have been saved!")
