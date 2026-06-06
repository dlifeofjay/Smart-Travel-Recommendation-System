import pandas as pd
from dummy_users import users
from predictor import predict
from association import associate
from recommendation_engine import recommendation_system

# main cleaned data from database
main_data = df = pd.read_csv(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\cleaned_data.csv")

# apply dummy users
user_data = users(main_data, unique_ratio=0.35)

# apply predictions
predict_data = predict(user_data)

# apply association
ass_data = associate(predict_data)

# recommend location and confidence
recommendation_system(predict_data, ass_data)

