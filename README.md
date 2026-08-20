# ETL Project – World's Largest Banks

## Overview

This project implements an automated ETL (Extract, Transform, Load) pipeline using Python to collect and process market capitalization data for the world's largest banks.

The project extracts bank data from a web page, converts market capitalization values from USD into GBP, EUR, and INR using provided exchange rates, and stores the processed data in CSV and SQLite database formats.

## Technologies Used

- Python
- Pandas
- NumPy
- BeautifulSoup
- Requests
- SQLite
- SQL

## ETL Process

### 1. Extract

Web scraping is used to extract bank names and market capitalization data from the "By market capitalization" table.

### 2. Transform

The market capitalization values are transformed from USD into:

- GBP
- EUR
- INR

The converted values are rounded according to the project requirements.

### 3. Load

The transformed dataset is:

- Saved as `Largest_banks_data.csv`
- Loaded into a SQLite database named `Banks.db`
- Stored in the `Largest_banks` table

## SQL Analysis

The project executes SQL queries to:

- Retrieve the complete bank dataset
- Calculate the average market capitalization in GBP
- Retrieve the top 5 banks

## Project Structure

```text
banks-etl-project/
│
├── banks_project.py
├── exchange_rate.csv
├── Largest_banks_data.csv
└── README.md
