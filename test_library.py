import pytest
from LibrarySyatem import (
    LibraryService, Book, BookCopy, Rack, User, Author, Publisher
)

@pytest.fixture
def library():
    """Initialize a library with 5 racks before each test."""
    return LibraryService(libraryId="L1", noOfRacks=5)

# -----------------------------
# USER TESTS
# -----------------------------

def test_add_user(library):
    library.addUser("U1", "Arpan")
    user = library.userService.findUser("U1")
    assert user is not None
    assert user.userName == "Arpan"
    assert len(library.userService.users) == 1

# -----------------------------
# BOOK & BOOKCOPY TESTS
# -----------------------------

def test_add_book_and_book_copies(library):
    status = library.addBook(
        bookId="B1",
        title="Python Basics",
        authors=["A1"],
        publishers=["P1"],
        bookcopyIds=["BC1", "BC2"]
    )

    assert status == ""   # racks sufficient
    book = library.bookService.findBook("B1")
    assert book.title == "Python Basics"
    assert len(book.bookCopies) == 2

    # Rack assigned
    assert book.bookCopies[0].rack is not None
    assert book.bookCopies[1].rack is not None

    # Author/Publisher linked
    assert book.authors[0].authorName == "A1"
    assert book.publishers[0].publisherName == "P1"


def test_add_book_when_racks_full(library):
    # fill 5 racks using 5 copies
    library.addBook("B1", "Book1", ["A"], ["P"], ["C1","C2","C3","C4","C5"])
    status = library.addBook("B2", "Book2", ["A"], ["P"], ["C6","C7"])
    assert status == "Racks are full so cpoies not added"

# -----------------------------
# BORROWING TESTS
# -----------------------------

def test_borrow_book_success(library):
    library.addUser("U1", "Arpan")
    library.addBook("B1", "Test Book", ["A1"], ["P1"], ["BC1"])

    msg = library.borrowBook("B1", "U1", "2025-01-01")
    assert msg == "Successfully borrowed book"

    book = library.bookService.findBook("B1")
    assert book.bookCopies[0].borrow is not None
    assert book.bookCopies[0].rack is None


def test_borrow_book_no_user(library):
    library.addBook("B1", "Test Book", ["A1"], ["P1"], ["BC1"])
    msg = library.borrowBook("B1", "UX", "2025-01-01")
    assert msg == "User is not Found"


def test_borrow_book_no_copy_available(library):
    library.addUser("U1", "Arpan")
    library.addUser("U2", "John")
    library.addBook("B1", "Test", ["A"], ["P"], ["BC1"])

    library.borrowBook("B1", "U1", "2025-01-01")
    msg = library.borrowBook("B1", "U2", "2025-01-01")
    assert msg == "BookCopy Not available"


def test_borrow_book_copy(library):
    library.addUser("U1","Arpan")
    library.addBook("B1", "Book", ["A"], ["P"], ["BC1"])

    msg = library.borrowBookCopy("BC1", "U1","2025-01-01")
    assert msg == "Book Borrowed Successfully"

    copy = library.bookCopyService.findBookCopy("BC1")
    assert copy.borrow.user.userId == "U1"
    assert copy.rack is None


# -----------------------------
# RETURNING TESTS
# -----------------------------

def test_return_book_copy(library):
    library.addUser("U1","Arpan")
    library.addBook("B1","Book",["A"],["P"],["BC1"])

    library.borrowBook("B1","U1","2025-01-01")
    msg = library.returnBookCopy("BC1")
    assert "Returned book copy BC1" in msg

    bookCopy = library.bookCopyService.findBookCopy("BC1")
    assert bookCopy.borrow is None
    assert bookCopy.rack is not None


# -----------------------------
# REMOVE BOOKCOPY TESTS
# -----------------------------

def test_remove_book_copy_not_found(library):
    msg = library.removeBookCopy("XX")
    assert msg == "Bookcopy is not available"


def test_remove_book_copy_when_borrowed(library):
    library.addUser("U1","Arpan")
    library.addBook("B1","Book",["A"],["P"],["BC1"])
    library.borrowBook("B1","U1","2025-01-01")

    msg = library.removeBookCopy("BC1")
    assert msg == "Book Copy already borrowed"


def test_remove_book_copy_success(library):
    library.addBook("B1","Book",["A"],["P"],["BC1"])
    msg = library.removeBookCopy("BC1")
    assert msg == "BookCopy Removed"


# -----------------------------
# SEARCH TESTS
# -----------------------------

def test_search_by_bookId(library):
    library.addBook("B1","Python",["A1"],["P1"],["BC1"])
    result = library.searchBook(type="id", bookId="B1")
    assert "B1 Python" in result
    assert "BC1" in result


def test_search_by_author(library):
    library.addBook("B1","Python",["Arpan"],["P"],["BC1"])
    result = library.searchBook(type="author", authorName="Arpan")
    assert "Python" in result
    assert "BC1" in result


def test_search_by_publisher(library):
    library.addBook("B1","Python",["A"],["Penguin"],["BC1"])
    result = library.searchBook(type="pub", publisherName="Penguin")
    assert "Python" in result
    assert "BC1" in result


# -----------------------------
# RACK TESTS
# -----------------------------

def test_rack_count(library):
    assert library.rackService.findNumberOfAvailableRacks() == 5
    library.addBook("B1","Test",["A"],["P"],["C1","C2"])
    assert library.rackService.findNumberOfAvailableRacks() == 3
