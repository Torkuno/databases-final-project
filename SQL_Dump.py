import mysql.connector
import csv
import os
from datetime import datetime

def mysql_dump_database_to_single_file(host, user, password, database, output_directory):
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    # Get a list of all tables in the database
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]

    # Get the current date and format it as a string
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Construct the output file name with the date
    output_file = os.path.join(output_directory, f"database_dump_{current_date}.csv")

    # Open a single CSV file to write all data
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)

        # Loop through all tables and dump each one into the same file
        for table in tables:
            # Query to select all data from the table
            query = f"SELECT * FROM {table}"
            cursor.execute(query)

            # Write a table header and the headers for the table
            csv_writer.writerow([f"Table: {table}"])
            csv_writer.writerow([i[0] for i in cursor.description])

            # Write the data for the table
            for row in cursor:
                csv_writer.writerow(row)

            # Write a separator after each table
            csv_writer.writerow(["--- End of Table: {table} ---"])

    # Close the cursor and connection
    cursor.close()
    conn.close()

# Example usage
mysql_dump_database_to_single_file('localhost', 'root', 'Miskinho_77', 'projectdb', 'Sqldumptest')