import pandas as pd
import os

class DataIO:
    """Handles all reading and writing of datasets."""
    
    @staticmethod
    def load_data(filepath):
        """Loads data and returns the DataFrame and its extension."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        ext = filepath.split('.')[-1].lower()
        if ext == 'csv':
            return pd.read_csv(filepath), ext
        elif ext == 'json':
            return pd.read_json(filepath), ext
        else:
            raise ValueError("Unsupported file format. Please use .csv or .json")

    @staticmethod
    def save_data(df, filepath, source_ext):
        """Saves data, forcing the output format to match the source format."""
        # Ensure the output filename uses the correct extension
        base_name = os.path.splitext(filepath)[0]
        final_filepath = f"{base_name}.{source_ext}"
        
        if source_ext == 'csv':
            df.to_csv(final_filepath, index=False)
        elif source_ext == 'json':
            df.to_json(final_filepath, orient='records', indent=4)
            
        return final_filepath