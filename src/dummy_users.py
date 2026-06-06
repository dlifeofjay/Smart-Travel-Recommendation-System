import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\cleaned_data.csv")

def users(df, unique_ratio=0.4):
    n_rows = len(df)
    
    # Number of unique customers
    n_unique = int(n_rows * unique_ratio)
    n_unique = max(50, min(n_unique, n_rows)) 
    
    print(f"Total rows: {n_rows}")
    print(f"Unique customers (1 to {n_unique}): {n_unique}")
    
    customer_ids = np.random.choice(
        a=np.arange(1, n_unique + 1), 
        size=n_rows, 
        replace=True                   
    )
    
    df["customer_id"] = customer_ids

    print("Created dummy users")
    
    return df

