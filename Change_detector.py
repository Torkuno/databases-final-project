import os
import pandas as pd
import csv
from datetime import datetime

def find_most_recent_files(directory):
    # List all files in the directory that start with 'database_dump_' and end with '.csv'
    files = [f for f in os.listdir(directory) if f.startswith('database_dump_') and f.endswith('.csv')]

    # Sort the files based on the date in their names (assuming the date is in the format YYYY-MM-DD)
    files.sort(key=lambda f: datetime.strptime(f[14:-4], '%Y-%m-%d'), reverse=True)

    # Return the two most recent files
    return files[:2]

def read_csv_robust(file_path):
    try:
        # Try to read the CSV file using pandas, skip bad lines if encountered
        return pd.read_csv(file_path, delimiter=',', on_bad_lines='skip')
    except Exception as e:
        # If an error occurs during reading, print an error message and return an empty DataFrame
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()

def read_tables_from_csv(file_path):
    tables = {}
    current_table = None
    current_data = []

    # Open the CSV file and read its contents line by line
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0].startswith("Table:"):
                # If a line starts with "Table:", it indicates the start of a new table
                if current_table and current_data:
                    # If there is a current table and data, create a DataFrame and add it to the tables dictionary
                    df = pd.DataFrame(current_data[1:], columns=current_data[0])
                    tables[current_table] = df
                current_table = row[0].split(':')[1].strip()
                current_data = []
            elif current_table and not row[0].startswith("--- End of Table"):
                # If there is a current table and the line does not start with "--- End of Table", add the row to current_data
                current_data.append(row)

    # Add the last table to the tables dictionary
    if current_table and current_data:
        df = pd.DataFrame(current_data[1:], columns=current_data[0])
        tables[current_table] = df

    return tables

def compare_tables(tables1, tables2):
    for table_name, df1 in tables1.items():
        df2 = tables2.get(table_name)

        if df2 is None:
            # If the table is in the first file but not in the second, print a message
            print(f"Table '{table_name}' found in the first file but not in the second.")
            continue

        # Ensure both dataframes have the same columns for comparison
        common_columns = df1.columns.intersection(df2.columns)
        df1_common = df1[common_columns].sort_index()
        df2_common = df2[common_columns].sort_index()

        # Compare the dataframes
        try:
            # Use pandas' compare function to find differences between the two dataframes
            comparison = df1_common.compare(df2_common, keep_shape=False, keep_equal=False)

            if not comparison.empty:
                # If there are differences, print details about the differences
                print(f"Differences in Table: {table_name}")
                for index, row in comparison.iterrows():
                    for col in comparison.columns.levels[0]:
                        old_value, new_value = row[(col, 'self')], row[(col, 'other')]
                        print(f"Row ID: {index}, Column: {col}, Old: {old_value}, New: {new_value}")
            else:
                # If no differences are found, print a message
                print(f"No differences found in Table: {table_name}")

        except ValueError as e:
            # If an error occurs during comparison, print an error message
            print(f"Error comparing tables '{table_name}': {e}")


def main():
    directory = "Sqldumptest"

    # Find the two most recent files in the specified directory
    recent_files = find_most_recent_files(directory)

    if len(recent_files) < 2:
        # If there are not enough files to compare, print a message and exit
        print("Not enough files to compare.")
        return

    # Get the file paths for the two most recent files
    file1, file2 = [os.path.join(directory, f) for f in recent_files]

    # Read tables from the CSV files
    tables1 = read_tables_from_csv(file1)
    tables2 = read_tables_from_csv(file2)

    # Compare the tables from the two files
    compare_tables(tables1, tables2)

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()
