# csv_writer.py

import pandas as pd
import os

class CSVWriter:
    def __init__(self, file_path):
        """
        Initialize the CSVWriter with the file path and remove existing file if it exists.

        Args:
            file_path (str): Path to the CSV file where records will be written.
        """
        self.file_path = file_path
        self.remove_existing_file()  # Check and remove file if it exists during initialization

    def remove_existing_file(self):
        """
        Check if the file exists and delete it if necessary.
        """
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
            print(f"Existing file {self.file_path} deleted.")

    @staticmethod
    def remove_and_flatten_dfs(info, key):
        """
        Flatten DataFrame fields and remove unnecessary fields from the info dictionary.

        Args:
            info (dict): The info dictionary.
            key (str): The key whose DataFrame content should be removed or flattened.

        Returns:
            dict: The updated info dictionary with the specified key removed or flattened.
        """
        if key in info and isinstance(info[key], (pd.DataFrame, dict, list)):
            if isinstance(info[key], pd.DataFrame):
                info[key] = info[key].to_dict(orient='records')
            elif isinstance(info[key], dict):
                info[key] = pd.json_normalize(info[key]).to_dict(orient='records')
            elif isinstance(info[key], list):
                info[key] = [pd.json_normalize(item).to_dict(orient='records') for item in info[key]]
        return info

    def write_record(self, record):
        """
        Write a single record to a CSV file. Records are appended to the file.

        Args:
            record: The record data, which could be a dictionary, a list, or a custom object.
        """
        try:
            if isinstance(record, dict):
                # Flatten the profiles field and remove unnecessary information if it's a dictionary
                record = self.remove_and_flatten_dfs(record, "profiles")
                record_df = pd.DataFrame([record])
            elif isinstance(record, list):
                # Convert list of dictionaries to DataFrame
                record_df = pd.DataFrame(record)
            else:
                # Handle custom object
                try:
                    # Extract attributes from custom object
                    record_data = {attr: getattr(record, attr) for attr in dir(record) if not attr.startswith('__')}
                    record_df = pd.DataFrame([record_data])
                except Exception as e:
                    print(f"Error converting record to DataFrame: {e}")
                    return

            # Check if file exists to determine whether to write headers
            file_exists = os.path.isfile(self.file_path)

            # Append the DataFrame to the CSV file
            record_df.to_csv(self.file_path, mode='a', header=not file_exists, index=False, encoding='utf-8')
            print(f"Record successfully written to {self.file_path}")

        except Exception as e:
            print(f"Error writing record to CSV: {e}")
