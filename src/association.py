from predictor import predict
import pandas as pd
import numpy as np
import os
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def associate(df):
    dfg = df.groupby(["predicted_season", "dep_city"])["arr_city"].apply(list).reset_index()
    df = dfg["arr_city"]

    te = TransactionEncoder()
    df_te = te.fit(df).transform(df)
    df = pd.DataFrame(df_te, columns=te.columns_)

    mdf = apriori(df, min_support=0.05, use_colnames=True)
    rules = association_rules(mdf, metric='lift', min_threshold=1.0)

    rl = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    df = rl[rl["confidence"] > 0.69]

    def clean_rules(rules):
        # Convert frozensets to clean strings
        rules = rules.copy()  # Avoid modifying original
        
        rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        
        return rules


    rl_clean = clean_rules(df)

    rl = rl_clean.sort_values('confidence', ascending=False).reset_index(drop=True)

    return rl[["antecedents", "consequents", "confidence"]]

