# Smart Travel Recommendation System

## Overview
This repository contains a **Smart Travel Recommendation System** that predicts travel patterns and generates personalized destination recommendations using machine learning and association rule mining. The system demonstrates a complete end‑to‑end ML pipeline:

1. **Data preprocessing** – aggregates raw airline booking data into customer profiles and augments with synthetic customer IDs.
2. **Season prediction** – a trained scikit‑learn classifier predicts the most likely travel season for each customer based on behavioral and demographic features.
3. **Association rule mining** – uses the Apriori algorithm to identify frequently co-occurring travel destinations and build association rules with high confidence.
4. **Recommendation engine** – applies association rules to suggest the next travel destination for each customer based on their past preferences and travel season.
5. **Interactive Streamlit UI** – allows users to query recommendations by client ID and view model performance metrics.

Built with Python, pandas, scikit-learn, MLxtend, joblib, and Streamlit.

---

## Directory Structure
```
Smart Travel Recommendation System/
├─ app.py                    # Streamlit web UI (recommendation system & model performance)
├─ README.md                 # This file
├─ artifact/                 # Serialized ML models and preprocessors
│   ├─ travel_model.pkl      # Trained season prediction classifier
│   ├─ feature_preprocessor.pkl # Feature encoder/scaler
│   └─ target_label.pkl      # Label encoder
├─ Notebooks/                # Jupyter notebooks for model development
│   ├─ Apriori Algorithm.ipynb        # Association rule mining exploration
│   └─ Travel Period Prediction.ipynb # Season prediction model training
├─ SQL & Database/           # Database and query files
│   ├─ SQLQuery1.sql         # SQL queries for data extraction from MSSQL database
│   └─ TRAVEL_ACTIVITIES.bak # SQL Server database backup file
├─ src/                      # Core pipeline modules
│   ├─ main.py               # Pipeline orchestrator
│   ├─ dummy_users.py        # Aggregates booking data by customer ID
│   ├─ predictor.py          # Season prediction on customer profiles
│   ├─ association.py        # Apriori algorithm for mining association rules
│   └─ recommendation_engine.py # Matches customers to rules & generates recommendations
└─ Travel Agency/            # Data files (input & output)
    ├─ cleaned_data.csv      # Input: cleaned booking records
    ├─ season_destination_lookup.csv # Seasonal destination reference
    ├─ airlines_lookup.csv
    ├─ airports_lookup.csv
    ├─ passengers.csv
    ├─ bookings.csv
    ├─ payments.csv
    ├─ segments.csv
    ├─ recommendations.json  # Output: customer-to-destination recommendations
    ├─ predict.npy           # Predicted season labels (for model evaluation)
    └─ true.npy              # True season labels (for model evaluation)
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
   pip install pandas numpy scikit-learn joblib streamlit mlxtend sqlalchemy pyodbc
   ```

---

## Database Setup

To run the pipeline with live database data:

1. **SQL Server Installation** (if not already installed)
   - Install SQL Server Express or Developer Edition
   - Install SQL Server Management Studio (SSMS)

2. **Restore Database Backup**
   - Open SQL Server Management Studio
   - Right-click **Databases** → **Restore Database**
   - Select device and navigate to `SQL & Database/TRAVEL_ACTIVITIES.bak`
   - Complete the restoration

3. **Verify Connection**
   - Update the connection string in the notebook if needed:
   ```python
   server = 'DESKTOP-74CHGLL\SQLEXPRESS'  # Change to your server name
   database = 'TRAVEL_ACTIVITIES'
   ```

4. **Run Data Pipeline**
   - Execute notebook: `Notebooks/Travel Period Prediction.ipynb`
   - This will extract data from the database, preprocess, and train the model

---

## How It Works

### Pipeline Stages

1. **Data Aggregation** (`dummy_users.py`)
   - Aggregates individual flight bookings into customer-level profiles
   - Groups numerical features (flight duration, cost, etc.) by mean
   - Groups categorical features (airline, cabin, city, etc.) by mode
   - Creates synthetic customer IDs to organize the booking data

2. **Season Prediction** (`predictor.py`)
   - Loads pre-trained scikit-learn classification model from `artifact/`
   - Applies feature preprocessing to customer profiles
   - Predicts travel season (e.g., summer, winter) for each customer
   - Outputs: predicted season label per customer

3. **Association Rule Mining** (`association.py`)
   - Groups destinations by predicted season and departure city
   - Uses MLxtend's Apriori algorithm to find frequent destination combinations
   - Generates association rules with high confidence (>0.69) using support and lift metrics
   - Creates rules like: "Customers who travel to City A in summer often also travel to City B"

4. **Recommendation Generation** (`recommendation_engine.py`)
   - Matches each customer's previous destination against association rules
   - Applies learned rules to suggest the next travel destination
   - Outputs: `recommendations.json` containing antecedents, consequents, and confidence scores for each customer

---

## Running the Pipeline

Execute the full recommendation pipeline:
```bash
python src/main.py
```

This will:
1. Load cleaned booking data from `Travel Agency/cleaned_data.csv`
2. Aggregate bookings into customer profiles
3. Predict travel seasons for each customer
4. Mine association rules from destination patterns
5. Generate recommendations and save to `Travel Agency/recommendations.json`

---

## Running the Streamlit Web UI

Launch the interactive Streamlit application:
```bash
streamlit run app.py
```

### Features

**Recommendation System Tab:**
- Enter a customer ID to view their travel history and personalized destination recommendation
- Displays the customer's most frequently visited destination
- Shows the recommended next destination based on association rules
- Displays confidence score of the recommendation

**Model Performance Tab:**
- Confusion matrix showing season prediction accuracy
- Classification report with precision, recall, and F1-scores
- Association rule statistics and data

---

## Model Training (Optional)

Pre-trained models are stored in `artifact/`. To retrain:
1. Prepare customer profile dataset with season labels
2. Use scikit-learn pipelines to train a multi-class classifier
3. Serialize the model and preprocessor with `joblib.dump()`
4. Update files in the `artifact/` folder

Refer to notebooks in `Notebooks/` for training examples.

---

## Generating Recommendations Programmatically

You can invoke the recommendation pipeline directly from Python:
```python
from src.recommendation_engine import recommendation_system
from src.predictor import predict
from src.association import associate
from src.dummy_users import users
import pandas as pd

# Load and preprocess data
df = pd.read_csv('Travel Agency/cleaned_data.csv')
cleaned_data = users(df, unique_ratio=0.35)

# Predict seasons
predict_data = predict(cleaned_data)

# Mine association rules
ass_data = associate(predict_data)

# Generate and save recommendations
recommendation_system(predict_data, ass_data)
```

The resulting recommendations are saved to `Travel Agency/recommendations.json`.

---

## Technologies Used

- **Python 3.x** – Core language
- **pandas** – Data manipulation and aggregation
- **numpy** – Numerical computations
- **scikit-learn** – Machine learning classification
- **MLxtend** – Apriori algorithm and association rules
- **joblib** – Model serialization
- **Streamlit** – Interactive web UI

---

## Contributing

Contributions are welcome. Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes with clear messages
4. Open a pull request against the `main` branch

Make sure any new code adheres to the existing style and includes appropriate documentation.

---

## License

This project is released under the MIT License. See the `LICENSE` file for details.
