import httpx
import pathlib

from data_pipelines import extract

def test_extract(monkeypatch):
    def mock_get(*args, **kwargs):
        text = pathlib.Path("open_library_api_response.json").read_text()
        return httpx.Response(200, text=text)

    monkeypatch.setattr(httpx, "get", mock_get)

    records = extract()
    first_record = next(records)

    assert first_record["title"] == "The Lord of the Rings"
