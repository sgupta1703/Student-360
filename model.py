import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib 

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)

    data['Study_Hours_Per_Day'].fillna(data['Study_Hours_Per_Day'].mean(), inplace=True)
    
    label_encoder = LabelEncoder()
    data['Stress_Level'] = label_encoder.fit_transform(data['Stress_Level'])
    
    scaler = StandardScaler()
    data[['Study_Hours_Per_Day', 'GPA']] = scaler.fit_transform(data[['Study_Hours_Per_Day', 'GPA']])

    return data

def train_model(data):
    X = data[['Study_Hours_Per_Day', 'Stress_Level']]  
    y = data['GPA']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')

    return model

def save_model(model, model_filename):
    joblib.dump(model, model_filename)
    print(f'Model saved to {model_filename}')

def load_model(model_filename):
    model = joblib.load(model_filename)
    return model

def predict_gpa(model, study_hours, stress_level):
    prediction = model.predict([[study_hours, stress_level]])  
    return prediction[0]

if __name__ == "__main__":
    file_path = 'data/student_lifestyle_dataset.csv'

    data = load_and_preprocess_data(file_path)

    model = train_model(data)

    save_model(model, 'student_gpa_predictor.pkl')

