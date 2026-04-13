import json
import logging
import re
from pathlib import Path

# Set up logging for clean console output
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def ingest_dynamic_data():
    """
    Scans the target directory for YYYY-MM-DD date folders, extracts JSON files,
    enriches the data with the folder date and page number, and consolidates it.
    """
    base_dir = Path("Ingest/data/raw/books")
    
    # Requirement: Target output directory
    output_file = Path("new_data/raw/books/ingest.json")
    all_books = []

    if not base_dir.exists():
        logging.error(f"Directory not found: {base_dir}")
        return

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    date_folders = [d for d in base_dir.iterdir() if d.is_dir() and date_pattern.match(d.name)]

    if not date_folders:
        logging.warning(f"No valid date folders (YYYY-MM-DD) found in {base_dir}")
        return

    for date_folder in date_folders:
        folder_date = date_folder.name
        logging.info(f"Processing data for date: {folder_date} ...")
        
        json_files = list(date_folder.glob("*.json"))
        
        for file_path in json_files:
            try:
                page_match = re.search(r"(\d+)", file_path.stem)
                page_number = int(page_match.group(1)) if page_match else None

                with open(file_path, 'r', encoding='utf-8') as file:
                    books_on_page = json.load(file)
                    
                    if isinstance(books_on_page, list):
                        for book in books_on_page:
                            book['source_date'] = folder_date
                            if page_number:
                                book['page_number'] = page_number
                            all_books.append(book)
                    else:
                        logging.warning(f"Skipping {file_path.name}: Expected a JSON array.")
                        
            except json.JSONDecodeError:
                logging.error(f"Skipping {file_path.name}: File is corrupted or invalid JSON.")
            except Exception as e:
                logging.error(f"Error processing {file_path.name}: {e}")

    try:
        # Requirement: Output directory should be created if it does not exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(all_books, out_file, indent=4)
        logging.info(f"Success! {len(all_books)} total books ingested and saved to {output_file}.")
    except Exception as e:
        logging.error(f"Failed to write to '{output_file}': {e}")

if __name__ == "__main__":
    ingest_dynamic_data()