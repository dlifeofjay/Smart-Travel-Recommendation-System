from datetime import datetime
import pandas as pd
import numpy as np
import joblib

# Load Artifacts
model = joblib.load(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\artifact\travel_model.pkl")
preprocessor = joblib.load(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\artifact\feature_preprocessor.pkl")
encoder = joblib.load(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\artifact\target_label.pkl")

# Expected feature order
feature_order = ['channel', 'trip_type', 'cabin', 'airline', 'origin', 'destination',
                 'pax_count', 'lead_time', 'passenger_type', 'gender',
                 'nationality', 'loyalty_member', 'payment_method', 'paid_usd',
                 'dep_airport', 'arr_airport', 'dep_city', 'arr_city', 'flight_duration',
                 'stop_type', 'Booking-Travel', 'Booking-Payment', 'Payment-Travel',
                 'Booking-dep', 'Payment-dep', 'Travel-dep', 'booking_year',
                 'booking_day', 'travel_year', 'travel_day', 'payment_year',
                 'payment_day', 'dep_year', 'dep_day']

def preprocess_data(df):
    # Group by customer_id - aggregate numerical as mean, categorical as mode
    agg_dict = {}
    
    # Numerical columns → mean
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    if 'customer_id' in num_cols:
        num_cols.remove('customer_id')
    for col in num_cols:
        agg_dict[col] = 'mean'
    
    # Categorical columns → mode (most frequent value)
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if 'season' in cat_cols:
        cat_cols.remove('season')
    for col in cat_cols:
        agg_dict[col] = lambda x: x.mode()[0] if not x.mode().empty else None
    
    # Perform groupby
    X = df.groupby('customer_id').agg(agg_dict).reset_index()

    # Keep original customer_id for later
    y = X['customer_id'].copy()
    
    # Reorder columns to match training
    X = X[feature_order]
    
    
    return X, y


def predict(df):
    X, customer_ids = preprocess_data(df)
    
    # Preprocess with saved preprocessor
    X_preprocessed = preprocessor.transform(X)
    
    # Predict
    y_pred = model.predict(X_preprocessed)
    y_pred_labels = encoder.inverse_transform(y_pred)
    
    # Add results
    X["predicted_season"] = y_pred_labels
    X["customer_id"] = customer_ids
    
    # Determine current season
    current_month = datetime.now().month
    if current_month in [6, 7, 8]:
        current_season = "Summer"
    elif current_month in [12, 1, 2]:
        current_season = "Winter"
    elif current_month in [3, 4, 5]:
        current_season = "Spring"
    else:
        current_season = "Autumn"
    
    # Filter by current season
    result = X[X["predicted_season"] == current_season].copy()
    
    print(f"Current Season: {current_season}")
    print(f"Total recommendations: {len(result)}")
    
    return result