import os
import sqlite3

import pytest

from alcazar.orm import Database, Table, Column, ForeignKey


class Author(Table):
    name = Column(str)
    age = Column(int)


@pytest.fixture
def db():
    DB_PATH = './test.db'
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = Database(DB_PATH)
    return db


class Book(Table):
    title = Column(str)
    published = Column(bool)
    author = ForeignKey(Author)


def test_create_db(db):
    assert isinstance(db.conn, sqlite3.Connection)
    assert db.tables == []


def test_define_tables():
    assert Author.name.type == str
    assert Book.author.table == Author

    assert Author.name.sql_type == 'TEXT'
    assert Author.age.sql_type == 'INTEGER'


def test_create_tables(db):
    db.create(Author)
    db.create(Book)

    assert Author._get_create_sql() == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER, name TEXT);"
    assert Book._get_create_sql() == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, published INTEGER, title TEXT);"

    for table in ('author', 'book'):
        assert table in db.tables


def test_create_author_instance(db):
    db.create(Author)

    john = Author(name="John Doe", age=35)

    assert john.name == "John Doe"
    assert john.age == 35
    assert john.id is None


def test_save_author_instances(db):
    db.create(Author)

    john = Author(name="John Doe", age=23)
    db.save(john)
    assert john._get_insert_sql() == (
        "INSERT INTO author (age, name) VALUES (?, ?);",
        [23, "John Doe"]
    )
    assert john.id == 1

    man = Author(name="Man Harsh", age=28)
    db.save(man)
    assert man.id == 2

    vik = Author(name="Vik Star", age=43)
    db.save(vik)
    assert vik.id == 3

    jack = Author(name="Jack Ma", age=39)
    db.save(jack)
    assert jack.id == 4


def test_query_all_authors(db):
    db.create(Author)
    john = Author(name="John Doe", age=23)
    vik = Author(name="Vik Star", age=43)
    db.save(john)
    db.save(vik)

    authors = db.all(Author)

    assert Author._get_select_all_sql() == (
        "SELECT id, age, name FROM author;",
        ["id", "age", "name"]
    )
    assert len(authors) == 2
    assert type(authors[0]) == Author
    assert {a.age for a in authors} == {23, 43}
    assert {a.name for a in authors} == {"John Doe", "Vik Star"}


def test_get_author(db):
    db.create(Author)
    roman = Author(name="John Doe", age=43)
    db.save(roman)

    john_from_db = db.get(Author, id=1)

    assert Author._get_select_where_sql(id=1) == (
        "SELECT id, age, name FROM author WHERE id = ?;",
        ['id', 'age', 'name'],
        [1]
    )
    assert type(john_from_db) == Author
    assert john_from_db.age == 43
    assert john_from_db.name == "John Doe"
    assert john_from_db.id == 1


def test_get_book(db):
    db.create(Author)
    db.create(Book)
    john = Author(name="John Doe", age=43)
    arash = Author(name="Arash Kun", age=50)
    book = Book(title="Building an ORM", published=False, author=john)
    book2 = Book(title="Scoring Goals", published=True, author=arash)
    db.save(john)
    db.save(arash)
    db.save(book)
    db.save(book2)

    book_from_db = db.get(Book, 2)

    assert book_from_db.title == "Scoring Goals"
    assert book_from_db.author.name == "Arash Kun"
    assert book_from_db.author.id == 2


def test_query_all_books(db):
    db.create(Author)
    db.create(Book)
    john = Author(name="John Doe", age=43)
    arash = Author(name="Arash Kun", age=50)
    book = Book(title="Building an ORM", published=False, author=john)
    book2 = Book(title="Scoring Goals", published=True, author=arash)
    db.save(john)
    db.save(arash)
    db.save(book)
    db.save(book2)

    books = db.all(Book)

    assert len(books) == 2
    assert books[1].author.name == "Arash Kun"


def test_update_author(db):
    db.create(Author)
    john = Author(name="John Doe", age=23)
    db.save(john)

    john.age = 43
    john.name = "John Wick"
    db.update(john)

    john_from_db = db.get(Author, id=john.id)

    assert john_from_db.age == 43
    assert john_from_db.name == "John Wick"


def test_delete_author(db):
    db.create(Author)
    john = Author(name="John Doe", age=23)
    db.save(john)

    db.delete(Author, id=1)

    with pytest.raises(Exception):
        db.get(Author, 1)
