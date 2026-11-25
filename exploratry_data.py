
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create customer churn dataset
data = {
    'CustomerID': [1,2,3,4,5,6,7,8,9,10],
    'Age': [25,30,35,np.nan,45,50,28,40,32,55],
    'MonthlyCharges': [200,300,250,400,np.nan,350,150,450,200,500],
    'Tenure': [1,12,24,6,36,48,3,60,18,72],
    'Churn': ['Yes','No','No','Yes','No','No','Yes','No','Yes','No']
}

df = pd.DataFrame(data)

# Display original data
print("Original Dataset:")
print(df)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Handle missing values
df['Age'] = df['Age'].fillna(df['Age'].mean())
df['MonthlyCharges'] = df['MonthlyCharges'].fillna(
    df['MonthlyCharges'].mean())

# Remove duplicate records
df = df.drop_duplicates()

# Summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Churn analysis
print("\nChurn Count:")
print(df['Churn'].value_counts())

# Average monthly charges by churn
print("\nAverage Monthly Charges:")
print(df.groupby('Churn')['MonthlyCharges'].mean())

# Visualization
df['Churn'].value_counts().plot(kind='bar')
plt.title("Customer Churn Analysis")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig("churn_analysis.png")
plt.show()

print("\nData Cleaning and EDA Completed!")
