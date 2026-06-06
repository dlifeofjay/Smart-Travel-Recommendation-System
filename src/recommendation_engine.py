import pandas as pd
import numpy as np
import json




def recommendation_system(data, rec_data):
    """
    Recommend destinations for current season
    based on association rules (Apriori)
    """
    
    # Initialize dict to collect id, past location, recommended location and confidence
    recom_dict = {}

    # Initialize for counts of location with existing city
    matched_count = 0
    
    # Loop for each user
    for i in range(len(data)):
        # each row is a user, so for each row give us the id and city they have been to
        customer_id = int(data["customer_id"].iloc[i])
        city = data["arr_city"].iloc[i]
        
        #Initialize city does not exist
        matched = False
        
        # loop each user through the recommendation dataset to find the city and recommended city of that city
        for j in range(len(rec_data)):
            # Get antecedents (city)
            antecedents = rec_data["antecedents"].iloc[j]
            
            # If city exist in each antecedent, get me the recommended next location
            if city in antecedents:
                # append to the above dict
                recom_dict[customer_id] = {
                    "antescedents": city,
                    "consequents": rec_data["consequents"].iloc[j],
                    "confidence": rec_data["confidence"].iloc[j]
                }
                # count because city exists
                matched = True
                matched_count += 1
                break   # Stop at first match
    
            # If otherwise, save recommendation as none
            else:
                recom_dict[customer_id] = {
                    "antescedents": city,
                    "consequents": None,
                    "confidence": 0.0,
                }

    print(f"Saved total of {matched_count} recommendations out of {len(data)}")

    # Save dictionary as json

    with open(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\recommendations.json", "w", encoding="utf-8") as f:
        json.dump(recom_dict, f, indent=4)

    print("Dictionary made and saved")
    print("All Done")









