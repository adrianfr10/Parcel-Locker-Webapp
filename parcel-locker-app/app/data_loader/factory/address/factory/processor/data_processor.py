from app.data_loader.factory.address.factory.data_factory import DataFactory
from typing import Any


class DataProcessor:
    """
    Processes data using components created by a DataFactory.
    """
    def __init__(self, data_factory: DataFactory) -> None:
        """
        Initializes the DataProcessor
        :param data_factory: An instance of DataFactory used to create data handling components.
        """
        self.data_loader = data_factory.create_data_loader()
        self.validator = data_factory.create_validator()
        self.converter = data_factory.create_converter()

    def process(self, path: str) -> list[Any]:
        """
        Processes the data using the components created by DataFactory.
        :param path: The path to the data source.
        :return: A list of processed data.
        """
        loader_data = self.data_loader.get_data(path)
        validated_data = [self.validator.validate(data) for data in loader_data]
        return [self.converter.convert(data) for data in validated_data]
