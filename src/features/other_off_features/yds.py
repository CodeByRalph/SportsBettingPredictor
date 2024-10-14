import numpy as np

def add_yds_features(df):

    # Rolling averages and sums for other stats
    df['REC_rolling_3'] = df['REC'].rolling(window=3, min_periods=1).mean()  # 3-game rolling average for REC
    df['TGTS_rolling_3'] = df['TGTS'].rolling(window=3, min_periods=1).mean()  # 3-game rolling average for TGTS
    df['TD_rolling_3'] = df['TD'].rolling(window=3, min_periods=1).mean()  # 3-game rolling average for TD
    
    df['REC_rolling_5'] = df['REC'].rolling(window=5, min_periods=1).mean()  # 5-game rolling average for REC
    df['TGTS_rolling_5'] = df['TGTS'].rolling(window=5, min_periods=1).mean()  # 5-game rolling average for TGTS
    df['AVG_rolling_5'] = df['AVG'].rolling(window=5, min_periods=1).mean()  # 5-game rolling average for AVG
    df['TD_rolling_5'] = df['TD'].rolling(window=5, min_periods=1).mean()  # 5-game rolling average for TD
    
    # Lag features for last game stats (to avoid leakage)
    df['REC_last_game'] = df['REC'].shift(1)
    df['TGTS_last_game'] = df['TGTS'].shift(1)
    df['AVG_last_game'] = df['AVG'].shift(1)
    df['TD_last_game'] = df['TD'].shift(1)
    df['LNG_last_game'] = df['LNG'].shift(1)

    df['LNG_squared'] = df['LNG'] * df['LNG']
    df['LNG_TGTS'] = df['LNG'] * df['TGTS']

    df['LNG_REC_interaction'] = df['LNG'] * df['REC']  # Interaction between longest reception and receptions
    df['AVG_REC_interaction'] = df['AVG'] * df['REC']

    # Cumulative stats over the season for other stats (excluding YDS)
    df['Cumulative_REC'] = df['REC'].cumsum()
    df['Cumulative_TGTS'] = df['TGTS'].cumsum()
    df['Cumulative_TD'] = df['TD'].cumsum()

    # Efficiency features (using receptions and targets)
    df['REC_to_TGTS'] = df['REC'] / df['TGTS'].replace(0, np.nan)  # Avoid divide by zero
    df['TD_per_REC'] = df['TD'] / df['REC'].replace(0, np.nan)  # Avoid divide by zero
    
    df['REC_TGTS_AVG'] = df['REC_to_TGTS'] * df['AVG']

    df['offensive_plays'] = df['REC'] + df['TGTS'] + df['CAR']  # Assuming CAR is carries/rushes
    df['YPT'] = df['YDS'] / df['TGTS'].replace(0, np.nan)




    # Fill NaN values from lagged features and efficiency metrics
    df.fillna(0, inplace=True)

    return df