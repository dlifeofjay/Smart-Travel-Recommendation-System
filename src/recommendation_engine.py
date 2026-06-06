import pandas as pd
import numpy as np
import json




def recommendation_system(data, rec_data):
    """
    Recommend destinations based on association rules (Apriori)
    """
    
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

    with open(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\recommendations.json", "w", encoding="utf-8") as f:
        json.dump(recom_dict, f, indent=4)

    print("Dictionary made and saved")
    print("All Done")









