import json
import logging
import pandas as pd
import re
from datetime import datetime
from pathlib import Path

# Set up logging to track the transformation process
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Dictionary to map text ratings to numbers
RATING_MAP = {
    "One": 1, 
    "Two": 2, 
    "Three": 3, 
    "Four": 4, 
    "Five": 5
}

def clean_price(price_str):
    """Aggressively strips all non-numeric characters (except decimals) to extract the price."""
    try:
        # This regex removes everything that is NOT a digit (\d) or a period (\.)
        # This prevents hidden web scraping characters (like Â£) from breaking the math
        clean_str = re.sub(r'[^\d.]', '', str(price_str))
        
        if clean_str:
            return float(clean_str)
        return None
    except (ValueError, TypeError):
        return None

def extract_book_id(url):
    """Extracts the numeric book_id from the URL string."""
    try:
        parts = str(url).split('/')
        for part in parts:
            if '_' in part:
                id_str = part.split('_')[-1]
                return int(id_str)
    except Exception:
        pass
    return None

def transform_data():
    """Reads ingested JSON, cleans and transforms fields, and exports a CSV."""
    input_file = Path("new_data/raw/books/ingest.json")
    output_file = Path("new_data/transformed/books/books_transformed.csv")
    base_url = "http://books.toscrape.com/catalogue/"

    logging.info(f"Loading raw data from {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"'{input_file}' not found. Please run ingest_data.py first.")
        return
    except json.JSONDecodeError:
        logging.error(f"'{input_file}' is empty or contains invalid JSON.")
        return

    # Load data into a Pandas DataFrame
    df = pd.DataFrame(data)

    if df.empty:
        logging.warning("No data found to transform.")
        return

    logging.info("Transforming data fields...")

    # 1. Convert Price to float using our bulletproof regex function
    if 'price' in df.columns:
        df['price'] = df['price'].apply(clean_price)

    # 2. Convert text Rating to numeric
    if 'rating' in df.columns:
        df['rating'] = df['rating'].map(RATING_MAP).fillna(0).astype(int)

    # 3. Convert Availability to binary flag (1 for in stock, 0 for out)
    if 'availability' in df.columns:
        df['availability'] = df['availability'].apply(
            lambda x: 1 if "in stock" in str(x).lower() else 0
        )

    # 4 & 5. Extract ID and construct Full URL
    if 'url' in df.columns:
        df['book_id'] = df['url'].apply(extract_book_id)
        df['url'] = df['url'].apply(
            lambda x: base_url + str(x).replace('catalogue/', '').lstrip('/')
        )

    # 6. Add Ingestion Timestamp
    df['ingestion_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Reorder columns to match the requested final structure
    expected_columns = [
        'book_id', 'title', 'price', 'rating', 'availability', 
        'url', 'page_number', 'source_date', 'ingestion_time'
    ]
    final_columns = [col for col in expected_columns if col in df.columns]
    
    df = df[final_columns]

    # Save to CSV
    logging.info(f"Saving transformed data to {output_file}...")
    try:
        # Create output directory if it does not exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_file, index=False, encoding='utf-8')
        logging.info(f"Success! {len(df)} book records transformed and saved.")
    except Exception as e:
        logging.error(f"Failed to save CSV file '{output_file}': {e}")

if __name__ == "__main__":
    transform_data()