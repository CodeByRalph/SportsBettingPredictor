import pandas as pd

"""
    File for creating custom features for data
"""

def add_moving_avg(df, length, stat):
    df[f'{length}_day_moving_avg_{stat}'] = df[f'{stat}'].rolling(window=length).mean()
    return df


def add_lag_features(df, stat, num_shift):
    df[f'{stat}_last_game'] = df[f'{stat}'].shift(num_shift)
    return df


def add_rolling_std(df, length, stat):
    df[f'{length}_day_rolling_std_{stat}'] = df[f'{stat}'].rolling(window=length).std()
    return df


def add_pct_change(df, stat):
    df[f'{stat}_pct_change'] = df[f'{stat}'].pct_change()

    return df



def engineer_features(df, stat):
    """
    Function gets called to add custom features to DataFrame

    Args:
        df (pd.DataFrame): The cleaned data
    
    Returns:
        pd.DataFrame: The processed DataFrame with all engineered features.
    """
    relevant_stats = ['CMP', 'ATT', 'YDS', 'CMP%', 'TD', 'INT', 'LNG', 'SACK'] # QBs
    #relevant_stats = ['REC', 'TGTS', 'YDS2', 'AVG', 'TD', 'CAR', 'FUM'] # RBs, Tightends, etc.

    # Moving Averages
    df = add_moving_avg(df, 3, 'INT')
    df = add_moving_avg(df, 7, 'INT')

    # lag features
    df = add_lag_features(df, 'CMP', 1)
    df = add_lag_features(df, 'ATT', 1)
    df = add_lag_features(df, 'INT', 1)

    df = add_lag_features(df, 'CMP', 5)
    df = add_lag_features(df, 'ATT', 5)
    df = add_lag_features(df, 'INT', 5)

    df = add_lag_features(df, 'CMP', 3)
    df = add_lag_features(df, 'ATT', 3)
    df = add_lag_features(df, 'INT', 3)



    # Rolling STD
    df = add_rolling_std(df, 14, 'YDS')
    df = add_rolling_std(df, 14, 'ATT')
    df = add_rolling_std(df, 10, 'CMP%')

    # Percent Change
    df = add_pct_change(df, 'YDS')

    # Interaction Features
    df['TD_LNG'] = df['TD'] * df['LNG']
    df['TD_SACK'] = df['TD'] + df['SACK']

    df['CMP/ATT'] = df['CMP'] / df['ATT']
    df['YPA'] = df['YDS'] * df['ATT']
    df['YPC'] = df['CMP'] * df['YDS']

    df['YDS_CMP%'] = df['YDS'] * df['CMP%']
    df['CMP*RTG'] = df['CMP'] * df['RTG']
    df['ATT_LNG'] = df['ATT'] * df['LNG']

    df['YDS_GAIN_EFF'] = (df['YDS'] / df['CMP']) * (df['TD'] / df['ATT']) * (1 / (df['INT']/ df['ATT']))
    df['Pressured_YDS'] = (df['YDS'] / df['ATT']) * (df['CMP%']) * (1 / (df['SACK'] / df['ATT']))

    df['ewma_YDS'] = df['YDS'].ewm(span=5, adjust=False).mean()  # 5-game weighted average
    df['ewma_CMP'] = df['CMP'].ewm(span=5, adjust=False).mean()

    df['AYA'] = (df['YDS'] + 20 * df['TD'] - 45 * df['INT']) / df['ATT']


    return df

