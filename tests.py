from main import BooksCollector
import pytest


class TestBooksCollector:

    @pytest.mark.parametrize("book_name", [
        "Короткий заголовок",
        "a" * 40,
    ])
    def test_add_new_book_valid_names(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()

    @pytest.mark.parametrize("book_name", [
        "a" * 41,
        "",
    ])
    def test_add_new_book_invalid_names(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_genre()

    def test_add_new_book_duplicate(self, collector):
        book_name = "Дубликат"
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == 1

    def test_set_book_genre_valid_case(self, collector):
        collector.add_new_book("Стражи галактики")
        collector.set_book_genre("Стражи галактики", "Фантастика")
        assert collector.get_book_genre("Стражи галактики") == "Фантастика"

    def test_set_book_genre_book_not_found(self, collector):
        collector.set_book_genre("Нет в коллекции", "Фантастика")
        assert collector.get_book_genre("Нет в коллекции") is None

    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book("Ведьмак")
        collector.set_book_genre("Ведьмак", "Неизвестный жанр")
        assert collector.get_book_genre("Ведьмак") == ""


    def test_get_book_genre_existing_book_with_genre(self, collector):
        book_name = "Острал"
        genre = "Ужасы"
        collector.add_new_book(book_name)
        collector.books_genre[book_name] = genre
        result = collector.get_book_genre(book_name)
        assert result == genre

    def test_get_book_genre_existing_book_without_genre(self, collector):
        collector.add_new_book("Без жанра")
        assert collector.get_book_genre("Без жанра") == ""

    def test_get_book_genre_nonexistent_book(self, collector):
        assert collector.get_book_genre("Нет в коллекции") is None


    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Супермен", "Звездные войны"]),
        ("Ужасы", ["Оно"]),
        ("Неизвестный жанр", []),
    ])
    def test_get_books_with_specific_genre(self, populated_collector, genre, expected_books):
        result = populated_collector.get_books_with_specific_genre(genre)
        assert sorted(result) == sorted(expected_books)


    def test_get_books_genre(self, collector):
        collector.add_new_book("ТРОН Арес")
        collector.set_book_genre("ТРОН Арес", "Фантастика")
        collector.add_new_book("Логан")
        expected = {
            "ТРОН Арес": "Фантастика",
            "Логан": ""
        }
        assert collector.get_books_genre() == expected


    def test_get_books_for_children(self, collector):
        books_data = [
            ("Зеркала", "Ужасы"),
            ("Шрек", "Мультфильмы"),
            ("Я и моя тень", "Комедии"),
        ]
        for book, genre in books_data:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)
        result = collector.get_books_for_children()
        assert "Шрек" in result                                                                
        assert "Я и моя тень" in result
        assert "Зеркала" not in result


    def test_add_book_in_favorites_valid_book(self, collector):
        collector.add_new_book("Перекресток")
        collector.add_book_in_favorites("Перекресток")
        assert "Перекресток" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_book_not_in_collection(self, collector):
        collector.add_book_in_favorites("Книга не в коллекции")
        assert "Книга не в коллекции" not in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate(self, collector):
        collector.add_new_book("Гари Потер")
        collector.add_book_in_favorites("Гари Потер")
        collector.add_book_in_favorites("Гари Потер")
        assert len(collector.get_list_of_favorites_books()) == 1


    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Играй как Бекхэм")
        collector.add_book_in_favorites("Играй как Бекхэм")
        collector.delete_book_from_favorites("Играй как Бекхэм")
        assert "Играй как Бекхэм" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_book_not_in_favorites(self, collector):
        collector.delete_book_from_favorites("Нет в избранном")
        assert "Нет в избранном" not in collector.get_list_of_favorites_books()


    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Веном")
        collector.add_new_book("Аквамен")

        collector.add_book_in_favorites("Аквамен")
        
        favorites = collector.get_list_of_favorites_books()
        assert "Аквамен" in favorites, "Книга 'Аквамен' должна быть в списке избранного"
        