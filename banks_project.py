from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime


def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open("code_log.txt", "a") as f:
        f.write(timestamp + " : " + message + "\n")


def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')

    df = pd.DataFrame(columns=table_attribs)

    tables = data.find_all('tbody')
    rows = tables[1].find_all('tr')

    for row in rows:
        col = row.find_all('td')

        if len(col) != 0:
            name = col[1].get_text(strip=True)
            market_cap = col[2].get_text(strip=True)

            if market_cap:
                market_cap = market_cap[:-1]
                market_cap = market_cap.replace(',', '')
                market_cap = float(market_cap)

                data_dict = {
                    "Name": name,
                    "MC_USD_Billion": market_cap
                }

                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df, df1], ignore_index=True)

    return df


def transform(df, csv_path):
    dataframe = pd.read_csv(csv_path)

    exchange_rate = dataframe.set_index('Currency').to_dict()['Rate']

    gbp_rate = float(exchange_rate['GBP'])
    eur_rate = float(exchange_rate['EUR'])
    inr_rate = float(exchange_rate['INR'])

    df['MC_GBP_Billion'] = [
        np.round(x * gbp_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    df['MC_EUR_Billion'] = [
        np.round(x * eur_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    df['MC_INR_Billion'] = [
        np.round(x * inr_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    return df


def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)


def load_to_db(df, sql_connection, table_name):
    df.to_sql(
        table_name,
        sql_connection,
        if_exists='replace',
        index=False
    )


def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)


# Main program

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"

table_attribs = ["Name", "MC_USD_Billion"]

csv_path = "./exchange_rate.csv"
output_path = "./Largest_banks_data.csv"

db_name = "Banks.db"
table_name = "Largest_banks"


# Task 1
log_progress("Preliminaries complete. Initiating ETL process")


# Task 2
df = extract(url, table_attribs)

log_progress("Data extraction complete. Initiating Transformation process")


# Task 3
df = transform(df, csv_path)

log_progress("Data transformation complete. Initiating Loading process")


# Task 4
load_to_csv(df, output_path)

log_progress("Data saved to CSV file")


# Task 5
sql_connection = sqlite3.connect(db_name)

log_progress("SQL Connection initiated")

load_to_db(df, sql_connection, table_name)

log_progress("Data loaded to Database as a table, Executing queries")


# Task 6

query_statement = "SELECT * FROM Largest_banks"
run_query(query_statement, sql_connection)

query_statement = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_query(query_statement, sql_connection)

query_statement = "SELECT Name FROM Largest_banks LIMIT 5"
run_query(query_statement, sql_connection)

log_progress("Process Complete")


# Task 7
sql_connection.close()

log_progress("Server Connection closed")