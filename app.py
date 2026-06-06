import streamlit as st
import pandas as pd
import numpy as np
import json
import random
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt

# Page navigation selector
page = st.sidebar.radio(
    "Navigation",
    ["Recommendation System", "Model Performance"]
)


# PAGE 1: RECOMMENDATION SYSTEM

if page == "Recommendation System":

    # Page header and description
    st.header("Smart Travel recommendation System")

    st.write("This project simulates how a machine learning recommendation system works in real time")

    st.write("System Layout: The system first predicts best time of the season a person will travel based on his behavioural and demographics features, then it uses data gathered to suggest or recommend best place he can travel based on popular market demand for that season and from the clients city")

    # Load recommendation data from JSON
    with open(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\recommendations.json", "r", encoding="utf-8") as f:
        recom_data = json.load(f)

    # Convert string keys to integers for lookup
    recom_data = {int(k): v for k, v in recom_data.items()}

    # Display statistics
    st.success(f"There are currently {len(recom_data):,} clients predicted to travel this summer")

    st.write("Enter Client ID to see most place they have been to and recommended next visit")

    # User input: client ID
    num = st.number_input(label="Enter ID", min_value=min(recom_data), max_value=max(recom_data))

    # Random client suggestion for invalid ID
    choice = random.choice(list(recom_data.keys()))

    # Get recommendation when button clicked
    if st.button("Recommendation"):
        if num not in recom_data.keys():
            st.error(f"Opps! Looks like this client doesn't travel out this period, why dont you try **{choice}**")
            
        else:
            rec = recom_data[num]
            
            # Case 1: No recommendation (cold start)
            if rec.get('consequents') is None:
                st.success(f"The most frequent place this client have been to is **{recom_data[num]['antescedents']}**")
                st.warning(f"Recommend **{recom_data[num]['antescedents']}** again, There is high chance they will go again this time of the season")
                
            # Case 2: Recommendation from association rules
            else:
                st.success(f"The most frequent place this client have been to is **{recom_data[num]['antescedents']}**")
                st.warning(f"People that have travelled to  **{recom_data[num]['antescedents']}** by this time of the season, have also travelled to **{recom_data[num]['consequents']}**")
                st.success(f"Recommend **{recom_data[num]['consequents']}** for the client")

    else:
        st.write("Click to get recommendation")



# PAGE 2: MODEL PERFORMANCE

else:

    st.title("Recommendation System Training Performance")

    st.header("Classification Model Performance")

    # Confusion matrix display
    st.subheader("Confusion Matrix")

    # Load prediction results
    pred = np.load(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\predict.npy")
    true = np.load(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\true.npy")

    # Plot confusion matrix
    fig, ax = plt.subplots()
    ConfusionMatrixDisplay.from_predictions(true, pred, ax=ax)
    ax.set_title("Confusion Matrix Display")
    st.pyplot(fig)

    # Classification metrics
    st.subheader("Classification Report")

    report = classification_report(true, pred)

    st.text(report)

    # Association rules visualization
    st.header("Recommendation System Layout")

    df = pd.read_csv(r"Travel Agency/Recommendation data.csv")

    st.write(df.head())