import httpx
import json

from data_pipelines import extract


class MockLibraryApiResponse:
    @staticmethod
    def json():
        with open("open_library_api_response.json") as f:
            data = json.load(f)

        return data


def test_extract(monkeypatch):
    def mock_get_json(*args, **kwargs):
        return MockLibraryApiResponse()

    monkeypatch.setattr(httpx, "get", mock_get_json)

    records = extract()
    first_record = next(iter(records))
    assert first_record["title"] == "The Lord of the Rings"
