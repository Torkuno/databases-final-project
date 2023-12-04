import os
import pandas as pd
import csv
from datetime import datetime

def find_most_recent_files(directory):
    files = [f for f in os.listdir(directory) if f.startswith('database_dump_') and f.endswith('.csv')]
    files.sort(key=lambda f: datetime.strptime(f[14:-4], '%Y-%m-%d'), reverse=True)
    return files[:2]

def read_csv_robust(file_path):
    try:
        return pd.read_csv(file_path, delimiter=',', on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()

def read_tables_from_csv(file_path):
    tables = {}
    current_table = None
    current_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0].startswith("Table:"):
                if current_table and current_data:
                    df = pd.DataFrame(current_data[1:], columns=current_data[0])
                    tables[current_table] = df
                current_table = row[0].split(':')[1].strip()
                current_data = []
            elif current_table and not row[0].startswith("--- End of Table"):
                current_data.append(row)

    # Add the last table
    if current_table and current_data:
        df = pd.DataFrame(current_data[1:], columns=current_data[0])
        tables[current_table] = df

    return tables

def compare_tables(tables1, tables2):
    for table_name, df1 in tables1.items():
        df2 = tables2.get(table_name)

        if df2 is None:
            print(f"Table '{table_name}' found in first file but not in second.")
            continue

        # Ensure both dataframes have the same columns for comparison
        common_columns = df1.columns.intersection(df2.columns)
        df1_common = df1[common_columns].sort_index()
        df2_common = df2[common_columns].sort_index()

        # Compare the dataframes
        try:
            comparison = df1_common.compare(df2_common, keep_shape=False, keep_equal=False)

            if not comparison.empty:
                print(f"Differences in Table: {table_name}")
                for index, row in comparison.iterrows():
                    for col in comparison.columns.levels[0]:
                        old_value, new_value = row[(col, 'self')], row[(col, 'other')]
                        print(f"Row ID: {index}, Column: {col}, Old: {old_value}, New: {new_value}")
            else:
                print(f"No differences found in Table: {table_name}")

        except ValueError as e:
            print(f"Error comparing tables '{table_name}': {e}")


def main():
    directory = "Sqldumptest"
    recent_files = find_most_recent_files(directory)
    if len(recent_files) < 2:
        print("Not enough files to compare.")
        return

    file1, file2 = [os.path.join(directory, f) for f in recent_files]

    tables1 = read_tables_from_csv(file1)
    tables2 = read_tables_from_csv(file2)

    compare_tables(tables1, tables2)

if __name__ == "__main__":
    main()
