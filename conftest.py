import pytest

from tests import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()


@pytest.fixture(scope="function")
def populated_collector():
    collector = BooksCollector()
    books_by_genre = {
        "Фантастика": ["Супермен", "Звездные войны"],
        "Ужасы": ["Оно"],
    }
    for genre_name, books in books_by_genre.items():
        for book in books:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre_name)
    return collector