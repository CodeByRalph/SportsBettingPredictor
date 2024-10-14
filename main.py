from src.data_fetching import fetch_multiple_logs
from src.data_cleaning import clean_data_for_model
from src.model_selection import test_model_performance
import pandas as pd
import os

if __name__ == "__main__":
    player_id = 3128390
    try:
        fetch_multiple_logs(player_id, 'rb', 2018, 2024)
        clean_data_for_model(player_id)
        test_model_performance(player_id, 'YDS')
    except Exception as e:
        print(f"Error occurred: {e}")
