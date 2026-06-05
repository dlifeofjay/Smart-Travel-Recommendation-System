from predictor import predict
import pandas as pd
import numpy as np
import json


df = pd.read_csv(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\cleaned_data_with_users.csv")
rec_data = pd.read_csv(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\Recommendation data.csv")


data = predict(df)

def recommendation_system(data, rec_data):
    """
    Recommend destinations based on association rules (Apriori)
    """
    # Load rules if path is given
    if isinstance(rec_data, str):
        rec_data = pd.read_csv(rec_data)
    
    recom_dict = {}
    matched_count = 0
    
    for i in range(len(data)):
        customer_id = int(data["customer_id"].iloc[i])
        city = data["arr_city"].iloc[i]
        
        matched = False
        
        for j in range(len(rec_data)):
            # Get antecedents
            antecedents = rec_data["antecedents"].iloc[j]
            
            # Check match
            if city in antecedents:
                recom_dict[customer_id] = {
                    "antescedents": city,
                    "consequents": rec_data["consequents"].iloc[j],
                    "confidence": rec_data["confidence"].iloc[j]
                }
                matched = True
                matched_count += 1
                break   # Stop at first match
    
            else:
                recom_dict[customer_id] = {
                    "antescedents": city,
                    "consequents": None,
                    "confidence": 0.0,
                }

    print(f"Saved total of {matched_count} recommendations out of {len(data)}")
    
    return recom_dict

recom_data = recommendation_system(data, rec_data)

with open(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\recommendations.json", "w", encoding="utf-8") as f:
    json.dump(recom_data, f, indent=4)







