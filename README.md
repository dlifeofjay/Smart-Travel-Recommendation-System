# Smart Travel Recommendation System

## Overview
This repository contains a **Smart Travel Recommendation System** that demonstrates how a machine‑learning pipeline can predict the optimal travel season for a client and generate destination recommendations based on association‑rule mining (Apriori algorithm). The project showcases a full end‑to‑end workflow:

1. **Data ingestion & preprocessing** – raw airline booking data is cleaned and augmented with synthetic user IDs.
2. **Season prediction model** – a trained scikit‑learn model predicts the most likely travel season for each customer.
3. **Recommendation engine** – association rules derived from historical trips suggest next‑visit destinations.
4. **Interactive UI** – a Streamlit app (`app.py`) lets users query recommendations by client ID.

The code is written in Python and uses common data‑science libraries (pandas, numpy, scikit‑learn, joblib) and Streamlit for the front‑end.

---

## Directory Structure
```
Smart Travel Recommendation System/
├─ .git/                     # Git repository metadata
├─ .gitignore                # Ignore patterns for Python and notebooks
├─ app.py                    # Streamlit entry point
├─ artifact/                 # Serialized model and preprocessing artifacts
│   ├─ travel_model.pkl
│   ├─ feature_preprocessor.pkl
│   └─ target_label.pkl
├─ Notebooks/                # Jupyter notebooks for exploration
│   ├─ Apriori Algorithm.ipynb
│   └─ Travel Period Prediction.ipynb
├─ src/                      # Core source code
│   ├─ dummy_users.py        # Generates synthetic customer IDs
│   ├─ predictor.py          # Loads model & makes season predictions
│   └─ recommendation_engine.py # Applies Apriori rules to suggest destinations
├─ Travel Agency/            # CSV/JSON data used by the pipeline
│   ├─ Main_data.csv
│   ├─ Recommendation data.csv
│   ├─ airlines_lookup.csv
│   ├─ airports_lookup.csv
│   ├─ bookings.csv
│   ├─ cleaned_data.csv
│   ├─ cleaned_data_with_users.csv
│   ├─ passengers.csv
│   ├─ payments.csv
│   ├─ recommendations.json
│   └─ segments.csv
├─ README.md                 # **This file**
└─ .ipynb_checkpoints/      # Notebook checkpoint files (auto‑generated)
```

---

## Installation
1. **Clone the repository**
   ```
   git clone https://github.com/dlifeofjay/Smart-Travel-Recommendation-System.git
   cd "Smart Travel Recommendation System"
   ```
2. **Create a virtual environment** (optional but recommended)
   ```
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   ```
3. **Install required packages**
   ```
   pip install -r requirements.txt
   ```
   If a `requirements.txt` is not present, install the core dependencies manually:
   ```
   pip install pandas numpy scikit-learn joblib streamlit
   ```

---

## Data Preparation
The `Travel Agency` folder already contains cleaned CSV files. If you wish to rebuild the intermediate files:
1. Run `src/dummy_users.py` to add a synthetic `customer_id` column to `cleaned_data.csv` and produce `cleaned_data_with_users.csv`.
2. Ensure the JSON file `recommendations.json` is present; it stores the Apriori association rules used by the recommendation engine.

---

## Model Training (Optional)
The pre‑trained model and preprocessors are stored in the `artifact` directory. To retrain:
1. Prepare a training dataset (`cleaned_data_with_users.csv`).
2. Use scikit‑learn pipelines to fit a classifier that predicts the travel season.
3. Serialize the model and preprocessing objects with `joblib.dump` and place them in the `artifact` folder.

---

## Running the Streamlit Application
The UI lets a user enter a client ID and view the most‑visited destination together with the next recommendation.
```bash
streamlit run app.py
```
Open the displayed localhost URL in a browser. Use the number input to select a client ID and click **Recommendation**.

---

## Generating Recommendations Programmatically
You can invoke the recommendation pipeline directly from Python:
```python
from src.recommendation_engine import recommendation_system
import pandas as pd

# Load data
df = pd.read_csv('Travel Agency/cleaned_data_with_users.csv')
rec_data = pd.read_csv('Travel Agency/Recommendation data.csv')

# Predict season and get recommendations
from src.predictor import predict
season_predictions = predict(df)
recommendations = recommendation_system(season_predictions, rec_data)
```
The resulting dictionary is saved to `Travel Agency/recommendations.json` by default.

---

## Contributing
Contributions are welcome. Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes with clear messages.
4. Open a pull request against the `main` branch.

Make sure any new code adheres to the existing style and includes appropriate documentation.

---

## License
This project is released under the MIT License. See the `LICENSE` file for details.
