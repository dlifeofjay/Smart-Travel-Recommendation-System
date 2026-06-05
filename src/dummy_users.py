import random
import os
import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\cleaned_data.csv")

# Create dummy customer id
def users(df):

    # Assumes we have 40% of total rows have unique customers to prompt repeat use of services
    length = int(len(df) * 0.4)
    df["customer_id"] = np.random.randint(1, length, size=len(df))
    return df, length

df, length = users(df)
print(df.head())
print(length)
print(df["customer_id"].nunique())

df.to_csv(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\cleaned_data_with_users.csv", index=False)