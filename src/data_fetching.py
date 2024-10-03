import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_player_game_log(player_id, year):
    """
    Scrapes regular season game log data for a given player and year, separating passing and rushing stats.
    """
    url = f'https://www.espn.com/nfl/player/gamelog/_/id/{player_id}/type/nfl/year/{year}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.espn.com/',
        'Connection': 'keep-alive',
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for player ID {player_id} in year {year}")
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables
    tables = soup.find_all('table', class_='Table')

    # Variable to hold the correct regular season table
    regular_season_table = None

    # Loop through the tables to find the one that contains "Regular Season"
    for table in tables:
        if "regular season" in table.text.lower():  # Check if 'Regular Season' appears in the table's text
            regular_season_table = table
            break

    # If we can't find the regular season table, raise an error
    if regular_season_table is None:
        raise Exception("Regular season table not found.")
    
    # Extract headers from the table and filter out unwanted ones
    table_header = table.find('thead').find_all('tr')
    stat_categories = table_header[1].find_all('th')
    headers = [th.get_text(strip=True) for th in stat_categories]

    # Changing duplicate headers
    header_count = {}
    resolved_headers = []

    for header in headers:
        if header in header_count:
            # Increment the count and append the count to the header name
            header_count[header] += 1
            resolved_headers.append(f"{header}{header_count[header]}")
        else:
            # If it's the first occurrence, just add it to the list and set the count to 1
            header_count[header] = 1
            resolved_headers.append(header)
    # DEBUG LINE - List of Headers    
    #print(resolved_headers)
    
    # Extract table rows from <tbody>
    rows = regular_season_table.find('tbody').find_all('tr')
    game_logs = []
    
    for row in rows:
        columns = row.find_all('td')
        
        # Create a dictionary for each row and ensure it's aligned with headers
        row_data = {}
        for i in range(len(resolved_headers)):
            # If there is a column for this header, assign the data, else assign None
            row_data[resolved_headers[i]] = columns[i].get_text(strip=True) if i < len(columns) else None
        
        game_logs.append(row_data)
    
    df = pd.DataFrame(game_logs)
    # DEBUG LINE - Final DataFrame
    #print(df)
    return df

def load_existing_game_logs(player_id, year):
    """
    Loads existing game log data for the player from CSV if it exists.
    """
    filepath = f"data/raw/player_{player_id}_{year}.csv"
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return None

def append_new_data(player_id, year):
    """
    Appends new data to the existing game log if there's new data available.
    """
    # Load existing data
    existing_data = load_existing_game_logs(player_id, year)
    
    # Scrape the latest game log data
    new_data = scrape_player_game_log(player_id, year)
    
    # If there is no existing data, save the new data directly
    if existing_data is None:
        save_game_log_data(player_id, year, new_data)
        print(f"Saved new data for {year} directly.")
        return
    
    # Compare the most recent game date in both datasets
    if not existing_data.empty:
        last_saved_game = existing_data.iloc[-1]['Date']
        new_data_to_append = new_data[new_data['Date'] > last_saved_game]
        
        # If there's new data, append it
        if not new_data_to_append.empty:
            updated_data = pd.concat([existing_data, new_data_to_append], ignore_index=True)
            save_game_log_data(player_id, year, updated_data)
            print(f"Appended new data for {year}.")
        else:
            print(f"No new data to append for {year}.")
    else:
        save_game_log_data(player_id, year, new_data)
        print(f"Saved new data for {year}.")

def save_game_log_data(player_id, year, df):
    """
    Saves game log data to a CSV file.
    """
    filepath = f"data/raw/player_{player_id}_{year}.csv"
    df.to_csv(filepath, index=False)
    print(f"Saved data to {filepath}.")

def fetch_multiple_logs(player_id, start_year, end_year):
    """
    Gathers game logs for a player across multiple years and ensures data is up to date.
    """
    for year in range(start_year, end_year + 1):
        append_new_data(player_id, year)