import os
import pandas as pd
import numpy as np
from src.data_fetching import load_existing_game_logs


def save_combined_logs(player_id, df):
    file_path = f'data/processed/player_{player_id}_clean.csv'
    df.to_csv(file_path, index=False)
    print(f"Saved Cleaned Data to {file_path}")




def combine_game_logs(player_id, directory = 'data/raw'):
    dataframes = []

    for filename in os.listdir(directory):
        # Check if the filename contains the player_id
        if f"player_{player_id}" in filename and filename.endswith(".csv"):
            # Build the file path
            file_path = os.path.join(directory, filename)
            year = os.path.basename(file_path).split('_')[-1].split('.')[0]
            #print(year)

            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            df['Date'] = df['Date'].astype(str) + '/' + year[2] + year[3]

            #print(df)
            # Append the DataFrame to the list
            dataframes.append(df)


    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        # Reformatting Date
        combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')
        return combined_df
    else:
        print(f"No CSV files found for player ID {player_id}")
        return pd.DataFrame()


def clean_data_for_model(player_id):
    df = combine_game_logs(player_id)

    # deletes rows that have NaT in Date field (Previously Regular Season)
    df = df.dropna(subset=['Date'])
    
    # Remove @ or vs in OPP
    df['OPP'] = df['OPP'].apply(lambda x: 1 if '@' not in x else 0)

    # replacing W with 1 and L with 0
    df['Result'] = df['Result'].apply(lambda x: 1 if 'W' in x else 0)

     # Drop columns where all values are '-' or non-numeric values
    df.replace('-', np.nan, inplace=True)
    df = df.dropna(axis=1, how='all')

    df = df.sort_values(by='Date', ascending=True)
    df = df.reset_index(drop=True)
    #print(df)

    save_combined_logs(player_id, df)
