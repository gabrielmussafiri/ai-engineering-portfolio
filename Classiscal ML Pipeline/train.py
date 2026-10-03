import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import numpy as np

from feature import engineer_features

load_dotenv()

DB_URL= f'postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'

engine = create_engine(DB_URL)

df = pd.read_sql('SELECT * FROM Transactions',engine)

df = engineer_features(df)
    

# Create Target : Is_anomaly
df['is_anomaly'] = (df['deviation'].abs()>2).astype(int)

print(df.dtypes)
print(f'\nTotal of row {len(df)}')
print(f'\nAnomaly distribution:\n{df["is_anomaly"].value_counts()}')
print(f'\nAny NAN? {df.isna().sum().sum()}')
print(f'\nAny Inf? {np.isinf(df.select_dtypes(include=np.number)).sum().sum()}')