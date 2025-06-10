import csv

def filter_csv(input_file, output_file, column_index, values_to_keep):
    """
    Extracts rows from a CSV file based on specific values in a column
    and saves them into a new CSV file.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        column_index (int): Index of the column to filter by.
        values_to_keep (list): List of values to keep in the specified column.
    """
    with open(input_file, 'r', newline='') as infile, \
            open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader) # Read the header
        writer.writerow(header) # Write header to the new file
        
        for row in reader:
            if row[column_index] in values_to_keep:
                writer.writerow(row)

# Example usage
input_csv = 'input.csv'
output_csv = 'output.csv'
column_to_filter = 2 # Example: filter the 3rd column (index 2)
values = ['value1', 'value2'] # Example values to keep in the column
filter_csv(input_csv, output_csv, column_to_filter, values)k