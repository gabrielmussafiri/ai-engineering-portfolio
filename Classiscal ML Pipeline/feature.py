
# Function to engineer features for the dataset
def engineer_features(df):
    # Feature Engineering
    df['user_avg_amount']  = df.groupby('user_id')['amount'].transform('mean')
    df['user_std_amount']  = df.groupby('user_id')['amount'].transform('std').fillna(1)
    df['user_std_amount'] = df['user_std_amount'].replace(0,1)
    df['user_txn_count'] = df.groupby('user_id')['amount'].transform('count')
    df['deviation'] = (df['amount'] - df['user_avg_amount']) / df['user_std_amount']
    df['hour_of_day'] =df['created_at'].dt.hour
    df['day_of_week']= df['created_at'].dt.dayofweek
    
    return df
    