import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def preprocess_data():
    data_path = "student_lifestyle_dataset.csv"
    data = pd.read_csv(data_path)
    data['Stress_Level'] = data['Stress_Level'].map({'Low': 0, 'Moderate': 1, 'High': 2})
    return data

def generate_visualizations(data):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='Study_Hours_Per_Day', y='GPA', data=data)
    plt.title('GPA vs Study Hours')
    plt.xlabel('Study Hours')
    plt.ylabel('GPA')
    plt.grid(True)
    plt.tight_layout()
    return plt
