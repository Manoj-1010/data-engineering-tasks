import pandas as pd

class DataProcessor:
    """Handles data ingestion, validation, and transformation logic."""
    
    def __init__(self, logger, data_io):
        self.logger = logger
        self.data_io = data_io

    def ingest(self, filepath):
        try:
            df, _ = self.data_io.load_data(filepath)
            self.logger.log(f"\n--- Ingestion Report: {filepath} ---")
            self.logger.log(f"Number of rows: {len(df)}")
            self.logger.log(f"Number of columns: {len(df.columns)}")
            self.logger.log("\nColumn Names:\n" + ", ".join(df.columns))
            self.logger.log("\nData Types:\n" + str(df.dtypes))
            self.logger.log("-" * 35 + "\n")
        except Exception as e:
            self.logger.log(f"Error ingesting data: {e}")

    def validate(self, filepath):
        try:
            df, _ = self.data_io.load_data(filepath)
            self.logger.log(f"\n--- Validation Report: {filepath} ---")
            
            # 1. Missing/Null values
            self.logger.log("1. Missing/Null Values:")
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if not missing.empty:
                self.logger.log(missing.to_string())
            else:
                self.logger.log("No missing values found.")

            # 2. Duplicate rows
            self.logger.log("\n2. Duplicate Rows:")
            duplicates = df.duplicated().sum()
            self.logger.log(f"Found {duplicates} exact duplicate row(s).")

            # 3. Inconsistent Data Types
            self.logger.log("\n3. Inconsistent Data Types:")
            inconsistencies_found = False
            for col in df.columns:
                if df[col].dtype == 'object':
                    types = df[col].dropna().apply(type).unique()
                    if len(types) > 1:
                        type_names = [t.__name__ for t in types]
                        self.logger.log(f" - Column '{col}' contains mixed types: {type_names}")
                        inconsistencies_found = True
            
            if not inconsistencies_found:
                self.logger.log("No immediate data type inconsistencies detected.")
            self.logger.log("-" * 35 + "\n")
            
        except Exception as e:
            self.logger.log(f"Error validating data: {e}")

    def transform(self, in_filepath, out_filepath):
        try:
            df, ext = self.data_io.load_data(in_filepath)
            self.logger.log(f"\n--- Transformation Process ---")
            
            # 1. Clean column names
            df.columns = df.columns.str.strip().str.lower().str.replace(r'\s+', '_', regex=True)
            self.logger.log("Standardized column names.")
            
            # 2. Remove duplicate records
            initial_rows = len(df)
            df = df.drop_duplicates()
            self.logger.log(f"Removed {initial_rows - len(df)} duplicate rows.")
            
            # 3. Handle missing values
            missing_count = df.isnull().sum().sum()
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna("Unknown")
            self.logger.log(f"Handled {missing_count} missing values.")

            # 4. Save cleaned data (forces correct extension based on input)
            final_path = self.data_io.save_data(df, out_filepath, ext)
            self.logger.log(f"\nSuccess: Cleaned data saved to {final_path}")
            self.logger.log("-" * 30 + "\n")
            
        except Exception as e:
            self.logger.log(f"Error transforming data: {e}")
