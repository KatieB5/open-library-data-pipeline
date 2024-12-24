import httpx
import csv
from collections import namedtuple
import itertools
import time

Book = namedtuple("Book", "title, author_name")


def main():
    records = extract()
    books = (transform(record) for record in records)
    generate_tsv(books, "book_titles_and_authors.csv")


def extract():
    params = {"q": "the lord of the rings", "page": 1, "limit": 50}
    response = httpx.get("https://openlibrary.org/search.json", params=params)
    response_dict = response.json()
    num_of_records = response_dict["numFound"]
    num_of_pages = num_of_records // params["limit"] + 1
    records = response_dict["docs"]
    yield from records
    for num in range(2, num_of_pages + 1):
        params["page"] = num
        time.sleep(1)
        response = httpx.get("https://openlibrary.org/search.json", params=params)
        records = response.json().get("docs")
        yield from records


def transform(record):
    an = record.get("author_name", "")
    author_name = [an] if isinstance(an, str) else an
    return Book(record["title"], ", ".join(author_name))


def generate_tsv(books, filename):
    book_0 = next(books)
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(book_0._fields)
        for book in itertools.chain([book_0], books):
            writer.writerow(book)


if __name__ == "__main__":
    main()
