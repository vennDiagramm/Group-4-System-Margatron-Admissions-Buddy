import os
import sqlite3
import pandas as pd

# Directory containing the CSV files
csv_directory = "C:/Users/Jhouvann/OneDrive/Desktop/College/2ND YEAR/PROG LANGUAGE/Chatbot/CSVS"

# Connect to the SQLite database
connection = sqlite3.connect("database1.db")
cursor = connection.cursor()

# Create the DataBase table to store 'Content' column from all CSVs
cursor.execute("CREATE TABLE IF NOT EXISTS DataBase (Content TEXT)")

# Loop through all CSV files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        csv_path = os.path.join(csv_directory, filename)
        try:
            # Read the CSV file
            df = pd.read_csv(csv_path, on_bad_lines='skip')

            # Check if the 'Content' column exists in the current CSV
            if 'Content' in df.columns:
                # Select only the 'Content' column, dropping any NaN entries
                df_content = df[['Content']].dropna()

                # Append the 'Content' column data to the 'DataBase' table
                df_content.to_sql("DataBase", connection, if_exists='append', index=False)
                print(f"Successfully added 'Content' column from {filename} to DataBase table")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Verify by fetching some data from the 'DataBase' table
cursor.execute("SELECT * FROM DataBase LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the database connection
connection.close()
