def add_att_features(df):

    df['YDS_per_CMP'] = df['YDS'] / (df['CMP'] + 1e-6)  # Adding a small value to avoid division by zero

    df['CMP_rolling_mean_3'] = df['CMP'].rolling(window=3).mean().fillna(df['CMP'].mean())

    df['CMP_rolling_std_3'] = df['CMP'].rolling(window=3).std().fillna(0)
    df['CMP_rolling_std_5'] = df['CMP'].rolling(window=5).std().fillna(0)

    df['Pass_to_Rush_Ratio'] = df['CMP'] / (df['CAR'] + 1e-6)

    df['YDS_to_SACK'] = df['YDS'] / (df['SACK'] + 1e-6)

    df['prev_CMP'] = df['CMP'].shift(1).fillna(df['CMP'].mean())
    df['prev_YDS'] = df['YDS'].shift(1).fillna(df['YDS'].mean())

    df['CMP_YDS_interaction'] = df['CMP'] * df['YDS']
    df['CMP_QBR_interaction'] = df['CMP'] * df['QBR']




    return df