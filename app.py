import pandas as pd
import pandas_datareader as data
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from keras.models import load_model
import streamlit as st
import seaborn as sns
import pickle
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import numpy as np
from sklearn.metrics import classification_report

st.title('Water Quality Prediction')

st.write('Give your data below')

with open('trained_model.pkl', 'rb') as f:
  model = pickle.load(f)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  st.write(df.describe())
  df.drop(df.columns[[0, 1, 5, 6, 7, 8, 9]], axis=1, inplace=True)
  df.head()
  df.drop(df.columns[[2]], axis=1, inplace=True)
  df.rename(columns={'field1': 'Turbidity', 'field2': 'ph', 'field3': 'tds'}, inplace=True)
  # df = df[['ph', 'tds', 'Turbidity']]
  predictions = model.predict_proba(df)
  predictions = np.where(predictions[:, 1] >= 0.5, 1, 0)
  potability = pd.DataFrame(predictions, columns=['Potability'])
  fig = px.scatter(df, x="ph", y="Turbidity", template="plotly_dark")
  st.write(fig)
  st.write(potability)



