import httpx
from collections import namedtuple

Book = namedtuple("Book", "title")


def main():
    records = extract()
    books = (transform(record) for record in records)
    for book in books:
        print(book.title)


def extract():
    response = httpx.get(
        "https://openlibrary.org/search.json?limit=10&q=the+lord+of+the+rings"
    )
    records = response.json().get("docs")
    yield from records


def transform(record):
    return Book(record["title"])


if __name__ == "__main__":
    main()
