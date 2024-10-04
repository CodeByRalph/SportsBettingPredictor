from src.data_fetching import fetch_multiple_logs
from src.data_cleaning import clean_data_for_model
import pandas as pd
import os

if __name__ == "__main__":
    player_id = 2577417  # Dak Prescott's ID as an example
    try:
        fetch_multiple_logs(player_id, 2021, 2023)
        clean_data_for_model(player_id)
    except Exception as e:
        print(f"Error occurred: {e}")
