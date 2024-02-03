from app.data_loader.factory.address.loader.data_loader import DataLoader
from typing import Any
import json


class JsonDataLoader(DataLoader):
    """
    Particular implementation of the DataLoader class used to load data from JSON
    file into a list
    """

    def get_data(self, filepath: str) -> list[dict[str, Any]]:
        """
        Loads data from a JSON file into a list of dicts
         Raises:
            AttributeError: If the file has an incorrect extension.
            FileNotFoundError: If the specified file is not found.
            json.decoder.JSONDecodeError: If the file has invalid JSON format or is empty.
        :param filepath:  The path to the JSON file.
        :return: A list of dictionaries representing the loaded data.
        """
        if not filepath.endswith('.json'):
            raise AttributeError('File has incorrect extension')
        try:
            with open(filepath, 'r') as jf:
                return json.load(jf)
        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError("File has invalid JSON format or file is empty", "", 0) from e
        except FileNotFoundError as e:
            raise FileNotFoundError(f'File not found: {e}')
        except Exception as e:
            print(f"Unexpected error: {e}")
