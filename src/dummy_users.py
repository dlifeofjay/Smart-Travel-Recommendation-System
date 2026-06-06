import pandas as pd
import numpy as np


def users(df, unique_ratio=0.4):

    """
    Create dummy repeat users,
    database doesnt have repeat users
    """
    n_rows = len(df)
    
    # Number of unique customers
    n_unique = int(n_rows * unique_ratio)
    n_unique = max(50, min(n_unique, n_rows)) 
    
    print(f"Total rows: {n_rows}")
    print(f"Unique customers (1 to {n_unique}): {n_unique}")
    
    # Create random customer id
    customer_ids = np.random.choice(
        a=np.arange(1, n_unique + 1), 
        size=n_rows, 
        replace=True                   
    )
    
    # Save result to a new column in the dataframe
    df["customer_id"] = customer_ids

    print("Created dummy users")
    
    return df

