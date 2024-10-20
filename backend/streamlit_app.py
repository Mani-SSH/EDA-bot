# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# Load your dataset
def load_data():
    return pd.read_csv('./camera_dataset.csv')

st.title("Clustering Analysis")

# Load the dataset
df = load_data()

st.header("Select Features for Clustering")
features = df.columns.tolist()
feature1 = st.selectbox("Select First Feature", features)
feature2 = st.selectbox("Select Second Feature", features)

if st.button("Run K-Means Clustering"):
    df_cleaned = df[[feature1, feature2]].dropna()
    kmeans = KMeans(n_clusters=3)
    df_cleaned['Cluster'] = kmeans.fit_predict(df_cleaned[[feature1, feature2]])

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_cleaned, x=feature1, y=feature2, hue='Cluster', palette='deep', s=100)
    plt.title('K-Means Clustering')
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.legend(title='Cluster')
    plt.grid()
    st.pyplot(plt)
