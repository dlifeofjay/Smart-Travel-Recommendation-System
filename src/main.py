import pandas as pd
from dummy_users import users
from predictor import predict
from association import associate
from recommendation_engine import recommendation_system

main_data = df = pd.read_csv(r"C:\Users\USER\Documents\MY PORTFOLIO\Smart Travel Recommendation System\Travel Agency\cleaned_data.csv")


cleaned_data = users(main_data, unique_ratio=0.35)

predict_data = predict(cleaned_data)

ass_data = associate(predict_data)

recommendation_system(predict_data, ass_data)

