from dataclasses import dataclass, field
class BookCopy:
    pass
class Borrow:
    pass
class Book:
    pass
class Author:
    pass
class Publisher:
    pass

@dataclass
class User:
    userId: str = None
    userName: str = None
    borrows: list[Borrow] = field(default_factory=list)
    
@dataclass
class Rack:
    rackId: str = None
    bookCopy: BookCopy = None

@dataclass
class BookCopy:
    borrow: Borrow = None
    rack: Rack = None
    bookCopyId: str = None
    book: Book = None

@dataclass
class Book:
    bookId: str = None
    title: str = None
    authors: list[Author] = field(default_factory=list)
    publishers: list[Publisher] = field(default_factory=list)
    bookCopies: list[BookCopy] = field(default_factory=list)

@dataclass
class Publisher:
    publisherName: str = None
    books: list[Book] = field(default_factory=list)

@dataclass
class Author:
    authorName: str = None
    books: list[Book] = field(default_factory=list)

@dataclass
class Borrow:
    user: User = None
    bookCopy: BookCopy = None
    dueDate: str = None

class BookService:
    def __init__(self):
        self.books :list[Book]= []

    def findBook(self, bookId):
        return next((i for i in self.books if i.bookId == bookId), None)
    
    def addBook(self,bookId):
        bookTemp = self.findBook(bookId)
        if bookTemp is None:
            book = Book()
            book.bookId=bookId
            self.books.append(book)
            return book
        else:
            return bookTemp
            
class BookCopyService:
    def __init__(self):
        self.bookCopies :list[BookCopy]= []
        pass

    def findBookCopy(self, bookCopyId)->BookCopy:
        return next((i for i in self.bookCopies if i.bookCopyId==bookCopyId), None)
    
    def removeBookCopy(self, bookCopyId):
        bookCopy = self.findBookCopy(bookCopyId) 
        if bookCopy is None:
            return "Bookcopy is not available"
        else:
            if bookCopy.borrow is not None:
                return "Book Copy already borrowed"
            rack = bookCopy.rack
            rack.bookCopy = None
            bookCopy.rack = None
            book = bookCopy.book
            book.bookCopies.remove(bookCopy)
        return "BookCopy Removed"
    
    def addBookCopy(self, bookCopyId)->BookCopy:
        bookCopy = self.findBookCopy(bookCopyId=bookCopyId)
        if bookCopy is None:
            tempBookCopy = BookCopy(bookCopyId=bookCopyId)
            self.bookCopies.append(tempBookCopy)
            return tempBookCopy
        else:
            return bookCopy

class UserService:
    def __init__(self):
        self.users :list[User] = []

    def findUser(self, userId:str):
        return next((i for i in self.users if i.userId == userId), None)
    
    def addUser(self,userId ,userName):
        user = self.findUser(userId=userId)
        if user is None: 
            user = User(userId=userId, userName = userName)
            self.users.append(user)
            return user
        else:
            return user

class AuthorService:
    def __init__(self):
        self.authors :list[Author] = []

    def findAuthor(self, name)->Author:
        return next((i for i in self.authors if i.authorName == name), None)
    
    def addAuthor(self, name :str):
        authorTemp = self.findAuthor(name)
        if  authorTemp is None:
            temp = Author(authorName=name)
            self.authors.append(temp)
            return temp
        else:
            return authorTemp

class PublisherService():
    def __init__(self):
        self.publishers :list[Publisher] = []

    def findPublisher(self, name)->Publisher:
        return next((i for i in self.publishers if i.publisherName == name), None)
    
    def addPublisher(self, name :str):
        publisherTemp = self.findPublisher(name)
        if  publisherTemp is None:
            temp = Publisher(publisherName=name)
            self.publishers.append(temp)
            return temp
        else:
            return publisherTemp

class RackService:
    def __init__(self,noOfRacks):
        self.racks :list[Rack] = [Rack(i,None) for i in range(noOfRacks)]
    def findNumberOfAvailableRacks(self):
        return sum(r.bookCopy is None for r in self.racks)
    def findFirstAvailableRack(self)->Rack:
        return next((i for i in self.racks if i.bookCopy is None), None)

class LibraryService:
    def __init__(self, libraryId, noOfRacks):
        self.rackService = RackService(noOfRacks=noOfRacks)
        self.bookService = BookService()
        self.bookCopyService = BookCopyService()
        self.authorService = AuthorService()
        self.publisherService = PublisherService()
        self.userService = UserService()
        self.libraryId = libraryId

    def addUser(self,userId, userName):
        self.userService.addUser(userId=userId,userName=userName)

    def addBook(self, bookId, title, authors, publishers, bookcopyIds):
        # If no rack available at all → return immediately
        if self.rackService.findNumberOfAvailableRacks() == 0:
            return "Racks are full so cpoies not added"
        
        book = self.bookService.addBook(bookId=bookId)
        status = ""

        # ---- Add Book Copies ----
        for copyId in bookcopyIds:
            rack = self.rackService.findFirstAvailableRack()
            if rack is None:
                status = "Racks are full so cpoies not added"
                break

            # Add or fetch book copy
            bookCopy = self.bookCopyService.addBookCopy(copyId)

            # Link both ways
            bookCopy.book = book
            book.bookCopies.append(bookCopy)

            rack.bookCopy = bookCopy   # FIX: previously missing
            bookCopy.rack = rack

        # ---- Book details ----
        book.title = title

        # ---- Authors ----
        authorsList = []
        for name in authors:
            author = self.authorService.addAuthor(name)
            if book not in author.books:       # Prevent duplicates
                author.books.append(book)
            authorsList.append(author)
        book.authors = authorsList

        # ---- Publishers ----
        publishersList = []
        for name in publishers:
            publisher = self.publisherService.addPublisher(name)
            if book not in publisher.books:    # Prevent duplicates
                publisher.books.append(book)
            publishersList.append(publisher)
        book.publishers = publishersList

        return status


        
    def removeBookCopy(self, bookCopyId):
        return self.bookCopyService.removeBookCopy(bookCopyId=bookCopyId)
        
    def borrowBook(self, bookId, userId, dueDate):
        user = self.userService.findUser(userId=userId)
        if user is None:
            return "User is not Found"
        book = self.bookService.findBook(bookId=bookId)
        bookCopies = book.bookCopies
        for i in bookCopies:
            if i.borrow is None:
                bookCopy = i
                borrow = Borrow(bookCopy=bookCopy,dueDate=dueDate,user=user)
                user.borrows.append(borrow)
                bookCopy.borrow = borrow
                bookCopy.rack = None
                return "Successfully borrowed book"
        return "BookCopy Not available"

    def borrowBookCopy(self, bookCopyId, userId, dueDate)->BookCopy:
        user = self.userService.findUser(userId=userId)
        if user is None:
            return "User Not available"
        bookCopy = self.bookCopyService.findBookCopy(bookCopyId=bookCopyId)
        if bookCopy is None:
            return "Bookcopy not available"
        if bookCopy.borrow is not None:
            return "Book borrowed by some other People"
        borrow = Borrow(user=user,bookCopy=bookCopy,dueDate=dueDate)
        user.borrows.append(borrow)
        bookCopy.borrow = borrow
        bookCopy.rack = None
        return "Book Borrowed Successfully"


    def returnBookCopy(self, bookCopyId)->str:
        bookCopy = self.bookCopyService.findBookCopy(bookCopyId=bookCopyId)
        if bookCopy is None:
            return "Invalid Bookcopy"
        rack = self.rackService.findFirstAvailableRack()
        if rack is None:
            return "Rack is Not available"
        rack.bookCopy = bookCopy
        bookCopy.rack = rack
        bookCopy.borrow = None
        return f"Returned book copy {bookCopyId} and added to rack: {rack.rackId}"

    def printBorrowed(self, userId)->str:
        user = self.userService.findUser(userId=userId)
        if user is None:
            return "User Not available"
        borrows = user.borrows
        temp = "Book Copy: "
        for i in borrows:
            temp += f"\n{i.bookCopy.bookCopyId} {i.dueDate}"
        temp += "\n"
        return temp

    def searchBook(self, type, bookId = None, authorName = None, publisherName = None):
        if bookId is not None:
            book = self.bookService.findBook(bookId=bookId)
            if book is None:
                return "Book not available"
            temp = "Book Copy: "
            for i in book.bookCopies:
                rack_id = i.rack.rackId if i.rack else "N/A"
                user_id = i.borrow.user.userId if i.borrow else "N/A"
                due_date = i.borrow.dueDate if i.borrow else "N/A"
                temp += f"\n{i.bookCopyId} {book.bookId} {book.title} {', '.join([auth.authorName for auth in book.authors])} {', '.join([pub.publisherName for pub in book.publishers])} {rack_id} {user_id} {due_date}"
            return temp
        if authorName is not None:
            author = self.authorService.findAuthor(name=authorName)
            if author is None:
                return "Author not available"
            books = author.books
            temp = "\nBook Copy: "
            for j in books:
                for i in j.bookCopies:
                    rack_id = i.rack.rackId if i.rack else "N/A"
                    user_id = i.borrow.user.userId if i.borrow else "N/A"
                    due_date = i.borrow.dueDate if i.borrow else "N/A"
                    temp += f"\n{i.bookCopyId} {j.bookId} {j.title} {', '.join([auth.authorName for auth in j.authors])} {', '.join([pub.publisherName for pub in j.publishers])} {rack_id} {user_id} {due_date}"
            return temp
        
        if publisherName is not None:
            publisher = self.publisherService.findPublisher(name=publisherName)
            if publisher is None:
                return "Publisher Not available"
            books = publisher.books
            temp = "\nBook Copy:"
            for book in books:
                for bookcopy in book.bookCopies:
                    rack_id = bookcopy.rack.rackId if bookcopy.rack else "N/A"
                    user_id = bookcopy.borrow.user.userId if bookcopy.borrow else "N/A"
                    due_date = bookcopy.borrow.dueDate if bookcopy.borrow else "N/A"
                    temp += f"\n{bookcopy.bookCopyId} {book.bookId} {book.title} {', '.join([auth.authorName for auth in book.authors])} {', '.join([pub.publisherName for pub in book.publishers])} {rack_id} {user_id} {due_date}"
            return temp
