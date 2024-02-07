import pytest
import os
import json.encoder

from app.data_loader.factory.address.loader.json_data_loader import JsonDataLoader


class TestDataLoaderJsonDataLoaderPathNotCorrect:

    @pytest.fixture()
    def incorrect_extension_path(self) -> str:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'test_file_wrong_extension.txt'))

    @pytest.fixture()
    def not_existing_path(self) -> str:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'file.json'))

    def test_when_path_has_incorrect_extension(self, incorrect_extension_path) -> None:
        with pytest.raises(AttributeError) as ae:
            loader = JsonDataLoader()
            loader.get_data(incorrect_extension_path)
        assert str(ae.value) == 'File has incorrect extension'

    def test_when_file_not_found(self, not_existing_path) -> None:
        with pytest.raises(FileNotFoundError) as e:
            loader = JsonDataLoader()
            loader.get_data(os.path.abspath(not_existing_path))
        assert str(e.value).startswith(f'File not found')


class TestDataLoaderJsonDataLoaderContentNotCorrect:
    @pytest.fixture()
    def addresses_empty_test_path(self) -> str:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'test_file_empty_entirely.json'))

    def test_when_file_has_no_content(self, addresses_empty_test_path) -> None:
        with pytest.raises(json.decoder.JSONDecodeError) as e:
            loader = JsonDataLoader()
            loader.get_data(addresses_empty_test_path)
        assert str(e.value).startswith("File has invalid JSON format or file is empty")


class TestDataLoaderJsonDataLoaderContentCorrect:
    @pytest.fixture()
    def addresses_valid_content(self) -> str:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'test_get_addresses_data.json'))

    def test_when_file_content_is_present(self, addresses_valid_content) -> None:
        loader = JsonDataLoader()
        result = loader.get_data(addresses_valid_content)
        assert 2 == len(result)
