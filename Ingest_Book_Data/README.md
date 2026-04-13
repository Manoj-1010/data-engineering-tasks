# 📚 Book Data ETL Pipeline & Dashboard

This is a complete End-to-End Data Engineering project that takes raw book data, cleans it up, and displays it in an interactive web dashboard. 

I built this project to practice extracting data, transforming it with Python, and visualizing it to find useful insights.

## 🛠️ What This Project Does

The project is split into three main phases:
1. **Data Ingestion (`ingest_data.py`):** Reads 50 different JSON files containing raw scraped book data and combines them into one single `ingest.json` file.
2. **Data Transformation (`transform_data.py`):** Cleans the messy data. It converts text prices into real numbers, changes text ratings into numbers (1-5), and cleans up the web links. The clean data is saved as `books_transformed.csv`.
3. **Data Dashboard (`app_dashboard.py`):** Uses Streamlit to create a visual dashboard showing pricing patterns, rating distributions, and stock availability.

## 🗂️ Project Structure

All the files are kept right in the main folder to keep things simple:

```text
book_etl_project/
├── data_page_1.json to data_page_50.json  # Raw input data
├── ingest_data.py                         # Step 1 script
├── transform_data.py                      # Step 2 script
├── app_dashboard.py                       # Step 3 script
├── run_pipeline.py                        # Master script to run everything
├── requirements.txt                       # List of Python libraries needed
└── README.md                              # Project instructions
