import numpy as np


def add_passing_yds_features(df):

    # Completion ratio (CMP / ATT)
    df['CMP_rate'] = df['CMP'] / df['ATT']
    df['CMP_ATT_rate'] = df['CMP_rate'] * df['ATT']
    df['CMP_rate_squared'] = df['CMP_rate'] ** 2

    # Calculate the rate of change (difference) in passer rating between games
    df['RTG_change'] = df['RTG'].diff().fillna(0)

    
    # Touchdown to attempt ratio (TD / ATT)
    #df['TD_to_ATT'] = df['TD'] / df['ATT']

    # Number of completions resulted in touchdown
    df['TD Efficiency'] = df['TD'] / df['CMP']
    
    df['INT_Efficiency'] = df['INT'] / df['CMP']

    # Interception to attempt ratio (INT / ATT)
    df['INT_to_ATT'] = df['INT'] / df['ATT']

    # Sack rate (SACK / ATT)
    #df['SACK_rate'] = df['SACK'] / df['ATT']

    # Replace zeroes in CMP with a small constant
    df['CMP'] = df['CMP'].replace(0, 1e-6)
    # Sack to completion ratio - high ratio = struggle under pressure
    df['SACK_to_CMP'] = df['SACK'] / df['CMP']

    # Pass-to-Rush Ratio
    df['ATT'] = df['ATT'].replace(0, 1e-6)
    # Replace zeroes in CAR with a small constant
    df['CAR'] = df['CAR'].replace(0, 1e-6)
    df['log_Pass_to_Rush_Ratio'] = np.log1p(df['ATT'] / df['CAR'])
    df['Rushing_Impact'] = df['YDS2'] / df['ATT']
    df['log_Rushing_Impact'] = np.log1p(df['YDS2'] / df['ATT'])

    df['ATT_Rushing_Impact_interaction'] = df['ATT'] * df['Rushing_Impact']


    # Rolling means for ATT (pass attempts) over 3 and 5 games (no leakage)
    df['ATT_rolling_mean_3'] = df['ATT'].rolling(window=3).mean()
    df['ATT_rolling_mean_5'] = df['ATT'].rolling(window=5).mean()

    df['ATT_rolling_std_3'] = df['ATT'].rolling(window=3).std()
    df['ATT_rolling_std_5'] = df['ATT'].rolling(window=3).std()


    # Rolling means for completion rate over 3 and 5 games (no leakage)
    df['CMP_rate_rolling_mean_3'] = df['CMP_rate'].rolling(window=3).mean()
    df['CMP_rate_rolling_mean_5'] = df['CMP_rate'].rolling(window=5).mean()

    df.drop(['TD'], axis=1)
    # Fill any NaN values that might arise from rolling windows
    df.fillna(0, inplace=True)

    return df