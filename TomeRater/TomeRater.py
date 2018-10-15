DEBUG = True


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}
        self.rating = None
        if DEBUG:
            print("USER: {0}".format(self.__repr__()))

    def get_email(self):
        return self.email

    def change_email(self, updated_address):
        self.email = updated_address
        print('{user}\'s email has been updated to: {email}'.format(user=self.name, email=self.email))
    
    def __repr__(self):
        return 'Customer Name: {name}, Customer Email: {email}, Customer Total Books Read: {books}.'.format(
            name=self.name, email=self.email, books=len(self.books))

    def __eq__(self, other_user):
        return self.name.lower() == other_user.name.lower() and self.email.lower() == other_user.email.lower()

    def read_book(self, book, rating=None):
        self.rating = rating
        self.books[book] = rating

    def get_average_rating(self):
        average = -1
        total = 0

        if len(self.books) > 0:
            for rating in self.books.values():
                if rating is not None:
                    total += rating
            average = total/len(self.books)

        return average


class Book(object):
    MAX_RATING = 5

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print('The book "{title}" ISBN has been updated : {isbn}'.format(isbn=self.isbn, title=self.title))

    def add_rating(self, rating):
        if rating in range(self.MAX_RATING):
            self.ratings.append(rating)
        else:
            print('This is an Invalid Rating! (rating = {rating})'.format(rating=rating))

    def __eq__(self, other_user):
        return self.title.lower() == other_user.title.lower() and self.isbn.lower() == other_user.isbn.lower()

    def get_average_rating(self):
        return sum(self.ratings) / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn):
        self.author = author
        super(Fiction, self).__init__(title=title, isbn=isbn)

    def get_author(self):
        return self.author

    def __repr__(self):
        return'{title} by {author}'.format(title=self.title, author=self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        self.subject = subject
        self.level = level
        super(Non_Fiction, self).__init__(title, isbn)

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format\
            (title=self.title, level=self.level, subject=self.subject)


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title=title, isbn=isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title=title, author=author, isbn=isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title=title, subject=subject, level=level, isbn=isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            self.users[email].read_book(book, rating)
            if rating is not None:  # RCH
                book.add_rating(rating)

            if book not in self.books.keys():
                self.books[book] = 0
            self.books[book] += 1

        else:
            print("No user with email {}".format(email))

    def add_user(self, name, email, books=None):
        self.users[email] = User(name, email)
        if books is not None:
            for book in books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        for key in self.books.keys():
            print(key)

    def print_users(self):
        for value in self.users.values():
            print(value)

    def get_most_read_book(self):
        return max(self.books, key=self.books.get)

    def highest_rated_book(self):
        average_ratings_books = {}
        for book in self.books:
            average_ratings_books[book.title] = book.get_average_rating()
        return max(average_ratings_books, key=average_ratings_books.get)

    def most_positive_user(self):
        average_ratings_user = {}
        for user in self.users.values():
            average_ratings_user[user.name] = user.get_average_rating()
        return max(average_ratings_user, key=average_ratings_user.get)

#Getting Creative!
#To take your project to the next level, choose/
#one of the following extension ideas to implement:

    def get_n_most_read_books(self, n):
        """
        Returns the n books which have been read the most in descending order.
        """
        if type(n) == int:
            books_sorted = [k for k in sorted(self.books, key=self.books.get, reverse=True)]
            return books_sorted[:n]
        else:
            print("The argument n = {n} is not of type int. Please pass an int.".format(n=n))

    def get_n_most_prolific_readers(self, n):
        """
        Returns the n readers which have read the most books in descending order.
        """
        if type(n) == int:
            readers = [(reader, reader.get_books_read()) for reader in self.users.values()]
            readers_sorted = [k[0] for k in sorted(readers, key=lambda reader: reader[1], reverse=True)]
            return readers_sorted[:n]
        else:
            print("The argument n = {n} is not of type int. Please pass an int.".format(n=n))

    def get_n_most_expensive_books(self, n):
        """
        Returns the n books which have the highest price in descending order.
        """
        if type(n) == int:
            books = {book: book.get_price() for book in self.books.keys()}
            books_sorted = [k for k in sorted(books, key=books.get, reverse=True)]
            return books_sorted[:n]
        else:
            print("The argument n = {n} is not of type int. Please pass an int.".format(n=n))

    def get_worth_of_user(self, user_email):
        """
        Determines the total price of all books read by the user associated
        with the user_email argument.
        """
        if user_email.find("@") == -1 or (user_email.find(".com") == -1 and user_email.find(".edu") == -1 and user_email.find(".org") == -1):
            print("The {email} is invalid, please ensure it has an @ and a .com, .edu, or .org domain.".format(email=user_email))
        else:
            user = self.users.get(user_email)
            if not user:
                print("User does not currently exist with email {email}. Please use an email for a valid user.".format(email=user_email))
            else:
                price = 0
                for book in user.books.keys():
                    price += book.get_price()
        return price