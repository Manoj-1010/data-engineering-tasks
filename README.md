# Data Engineering Tasks

## Task 1: Excel Mapping
Load data from source Excel file and map monthly data to output template by month abbreviation. Extracts revenue values and populates corresponding columns.

## Task 2: Excel Consolidation
Consolidate multi-month MIS data (April/May/June) into a single output file. Extracts revenue per project from source files and populates output columns D (Apr), G (May), J (Jun).

## Task 3: CLI Data Processing Tool
Interactive command-line utility for CSV/JSON data processing with three operations:

- `ingest`: Display dataset metadata (rows, columns, data types)
- `validate`: Check data quality (missing values, duplicates, type consistency)
- `transform`: Clean and export data (normalize columns, remove duplicates, handle nulls)
