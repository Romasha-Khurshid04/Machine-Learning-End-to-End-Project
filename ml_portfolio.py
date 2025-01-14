# -*- coding: utf-8 -*-
"""ML Portfolio.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SfUet9P8KTFb9buYV6htnz6Pag6xaUTK
"""

#Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
!pip install gradio

"""**Part**#**01** **Data** **Cleaning**"""

df=pd.read_csv('/content/Student Depression Dataset.csv')
df.tail(50)

df.columns

df.info()

df.isnull().sum()

df['Sleep Duration'] = (df['Sleep Duration']
                         .str.replace('Less than 5', '3.5', regex=False)
                         .str.replace('More than 8', '9.5', regex=False)
                         .str.replace('Others', '0', regex=False)
                         .str.replace('5-6', '5.5', regex=False)
                         .str.replace('7-8', '7.5', regex=False)
                         .str.replace(' hours', '', regex=False))

df['Dietary Habits'] = (df['Dietary Habits']
                         .str.replace('Healthy', '1', regex=False)
                         .str.replace('Unhealthy', '0', regex=False)
                         .str.replace('Others', 'NaN', regex=False)
                         .str.replace('Moderate', '0.5', regex=False))

df.rename(columns={'Family History of Mental Illness': 'Family History'}, inplace=True)
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
df['Family History'] = df['Family History'].map({'Yes': 1, 'No': 0})
df['Have you ever had suicidal thoughts ?'] = df['Have you ever had suicidal thoughts ?'].map({'Yes': 1, 'No': 0})

df = df.astype({'Gender': 'int', 'Age': 'int','Family History':'int','Have you ever had suicidal thoughts ?':'int','Sleep Duration':'float','Dietary Habits':'float'})

df['City'] = (df['City']
                         .str.replace('City', 'NaN', regex=False)
                         .str.replace('3.0', 'NaN', regex=False)
                         .str.replace('Less than 5', '', regex=False)
                         .str.replace('ME', 'NaN', regex=False)
                         .str.replace('M.Com', 'NaN', regex=False)
                         .str.replace('Less', '', regex=False)
                         .str.replace('M.Tech', 'NaN', regex=False))
df['City'].isnull().sum()

df=df.dropna()

df.info()
df['Degree'].unique()

education_mapping = {
    'Class 12': 12,
    'BSc': 14,'BA':14,'B.Ed':14,'B.Com':14,'B.Tech':14,
    'BCA':16,'M.Tech':16,'B.Pharm':16,'BE':16,'M.Com':16,'BBA':16,'M.Ed':16,'MSc':16,'B.Arch':16,'BHM':16,'MA':16,
    'M.Pharm': 18,'MCA':18,'ME':18,'MHM':18,'MD':18,'MBA':18,'LLB':15,
    'MBBS':17,'LLM':17, 'PhD': 20,'Others':0
}
df['Degree'] = df['Degree'].map(education_mapping)

df['Degree'].astype(int)

df['Profession'].unique()

Encoder=LabelEncoder()
df['Profession']=Encoder.fit_transform(df['Profession'])
df=df.drop('id',axis=1)
df=df.drop('City',axis=1)
df.head()

df.to_csv('cleaned_data.csv', index=False)

"""**Part**#**02** **Model** **Building**"""

x=df.drop('Depression',axis=1)
y=df['Depression']

x.hist(figsize=(15,10),bins=10)
plt.tight_layout()
plt.show()

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model=LogisticRegression()
model.fit(X_train,y_train)
x.info()

y_pred = model.predict(X_test)
# Print the accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))
# Print the confusion matrix
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

"""**Part**#**03** **Model** **Saving** **and** **Loading**"""

import joblib
joblib.dump(model, 'Logistic_Regression.pkl')
loaded_model = joblib.load('Logistic_Regression.pkl')

def predict(Gender, Age, Profession, Academic_Pressure, Work_Pressure, CGPA, Study_Satisfaction,
            Job_Satisfaction, Sleep_Duration, Dietary_Habits, Degree, Suicidal_Thoughts,
            Work_Study_Hours, Financial_Stress, Family_History):
    # Prepare the input features in the correct format
    input_features = [[Gender, Age, Profession, Academic_Pressure, Work_Pressure, CGPA, Study_Satisfaction,
                       Job_Satisfaction, Sleep_Duration, Dietary_Habits, Degree, Suicidal_Thoughts,
                       Work_Study_Hours, Financial_Stress, Family_History]]

    # Predict using the model
    result = loaded_model.predict(input_features)

    # Output the result
    if result == 1:
        print("Person has depression")
    else:
        print("Person has no depression")

# Example usage
predict(1,20,11,5.0,0.0,8.97,2.0, 0.0,3.5,1.0,16,1,3.0,0.5,1)

"""**Part**#**04** **Interface**"""

import gradio as gr
demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="Gender"),
        gr.Number(label="Age"),
        gr.Number(label="Profession"),
        gr.Number(label="Academic Pressure"),
        gr.Number(label="Work Pressure"),
        gr.Number(label="CGPA"),
        gr.Number(label="Study Satisfaction"),
        gr.Number(label="Job Satisfaction"),
        gr.Number(label="Sleep Duration"),
        gr.Number(label="Dietary Habits"),
        gr.Number(label="Degree"),
        gr.Number(label="Suicidal Thoughts (1: Yes, 0: No)"),
        gr.Number(label="Work/Study Hours"),
        gr.Number(label="Financial Stress"),
        gr.Number(label="Family History")
    ],
    outputs=gr.Text(label="Depression Status")
)

# Launch the Gradio interface
demo.launch(debug=True)

