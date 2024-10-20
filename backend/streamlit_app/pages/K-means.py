import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from Index import load_data
from sklearn.cluster import KMeans

st.title("K-means Clustering")
st.write("This is the K-means Clustering page.")
from sklearn.preprocessing import LabelEncoder

df = load_data()

with st.sidebar:
    st.title('K-Means settings')
    k_mean_value = st.slider("Number of Clusters",1,10,3,1)
    variable1 = st.selectbox("Variable 1",df.columns, index=0)
    variable2 = st.selectbox("Variable 2",df.columns, index=1)
    run_button = st.button("Run K-Means")

# Convert categorical variables to numeric
for col in [variable1, variable2]:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])

# Drop rows with missing values if necessary
df = df.dropna(subset=[variable1, variable2])

if (run_button):
    # Run K-Means
    kmeans = KMeans(n_clusters=k_mean_value)
    df['Cluster'] = kmeans.fit_predict(df[[variable1, variable2]])

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.scatter(df[variable1], df[variable2], c=df['Cluster'], cmap='viridis', s=100)
    plt.title(f"K-Means Clustering with {k_mean_value} Clusters")
    plt.xlabel(variable1)
    plt.ylabel(variable2)
    plt.colorbar(label='Cluster')
    st.pyplot(plt)
    
