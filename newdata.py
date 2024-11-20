import os
from pathlib import Path
import zipfile
import urllib.request
import pandas as pd
from shutil import move, rmtree
from datetime import datetime

def filter_and_quote_columns(input_file, required_columns, columns_to_quote):
    """
    Filters the CSV to include only required columns, converts specific columns to strings with quotes,
    and overwrites the input CSV file.
    """
    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Filter for required columns
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Some required columns are missing in the input file")
    df = df[required_columns]
    
    # Convert specific columns to strings and wrap in double quotes
    for col in columns_to_quote:
        if col in df.columns:
            df[col] = '"' + df[col].astype(str) + '"'
        else:
            raise ValueError(f"Column '{col}' to quote is not in the required columns list")

    # Overwrite the original CSV file
    df.to_csv(input_file, index=False, quotechar='"', quoting=3)  # quoting=3 disables automatic quoting
    print(f"Processed and saved updates to {input_file}")

def process_zip(endpoint_url, exclude_files, destination_folder):
    try:
        # Create unique temp folder for download and extraction
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        temp_folder = Path(f"down_{timestamp}")
        temp_folder.mkdir(parents=True, exist_ok=True)
        extract_to = temp_folder
        zip_file_path = temp_folder / "f1db_csv.zip"

        # 1. Download the ZIP file
        try:
            print(f"Downloading ZIP file from {endpoint_url}...")
            urllib.request.urlretrieve(endpoint_url, zip_file_path)
            print(f"Downloaded ZIP file to {zip_file_path}")
        except Exception as e:
            print(f"Failed to download ZIP file: {e}")
            return  # Exit the function as further steps depend on this file

        # 2. Extract the ZIP file
        try:
            print(f"Extracting ZIP file to {extract_to}...")
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print("Extraction completed.")
        except zipfile.BadZipFile:
            print("The downloaded file is not a valid ZIP file. Aborting.")
            return
        except Exception as e:
            print(f"Error extracting ZIP file: {e}")
            return

        # 3. Delete the ZIP file after extraction
        try:
            zip_file_path.unlink()
            print(f"Deleted ZIP file: {zip_file_path}")
        except Exception as e:
            print(f"Error deleting ZIP file: {e}")

        # 4. Process `races.csv` if present-----------------------------------------------------------------------------------
        try:
            races_file = temp_folder / "races.csv"
            if races_file.exists():
                required_columns = ['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time', 'url']
                columns_to_quote = ['name', 'date', 'time', 'url']
                print(f"Processing {races_file} in temporary folder...")
                filter_and_quote_columns(races_file, required_columns, columns_to_quote)
            else:
                print("races.csv not found in the extracted files.")
        except Exception as e:
            print(f"Error processing races.csv: {e}")
            return

        # 5. Delete all files except the excluded ones-----------------------------------------------------------------------
        try:
            print("Deleting non-excluded files...")
            for file in extract_to.iterdir():
                if file.is_file() and file.name not in exclude_files:
                    file.unlink()  # Delete non-excluded files
                    print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Error during file cleanup: {e}")
            return

        # 6. Move remaining files to the destination folder, overwriting if necessary
        destination_folder = Path(destination_folder)
        destination_folder.mkdir(parents=True, exist_ok=True)
        print("Moving remaining files to destination folder...")
        for file in extract_to.iterdir():
            if file.is_file():  # Move only remaining (excluded) files
                target_path = destination_folder / file.name
                if target_path.exists():
                    target_path.unlink()  # Overwrite existing files
                move(str(file), target_path)
                print(f"Moved file: {file} to {target_path}")
        
        # 7. Delete the temporary folder
        try:
            rmtree(temp_folder)
            print(f"Deleted temporary folder: {temp_folder}")
        except Exception as e:
            print(f"Error deleting temporary folder: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Define variables
endpoint_url = "https://ergast.com/downloads/f1db_csv.zip"  
exclude_files = {"circuits.csv", "constructors.csv", "drivers.csv", "races.csv"}  # Files to retain
destination_folder = "db"  # TODO: change the folder

# Process the ZIP file
process_zip(endpoint_url, exclude_files, destination_folder)
