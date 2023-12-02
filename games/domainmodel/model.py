from datetime import datetime


class Publisher:
    def __init__(self, publisher_name: str):
        if publisher_name == "" or type(publisher_name) is not str:
            self.__publisher_name = None
        else:
            self.__publisher_name = publisher_name.strip()

    @property
    def publisher_name(self) -> str:
        return self.__publisher_name

    @publisher_name.setter
    def publisher_name(self, new_publisher_name: str):
        if new_publisher_name == "" or type(new_publisher_name) is not str:
            self.__publisher_name = None
        else:
            self.__publisher_name = new_publisher_name.strip()

    def __repr__(self):
        return f"<Publisher {self.__publisher_name}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.publisher_name == self.__publisher_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__publisher_name < other.publisher_name

    def __hash__(self):
        return hash(self.__publisher_name)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self) -> str:
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.genre_name == self.__genre_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__genre_name < other.genre_name

    def __hash__(self):
        return hash(self.__genre_name)


class Game:
    def __init__(self, game_id: int, game_title: str):
        if type(game_id) is not int or game_id < 0:
            raise ValueError("Game ID should be a positive integer!")
        self.__game_id = game_id

        if type(game_title) is str and game_title.strip() != "":
            self.__game_title = game_title.strip()
        else:
            self.__game_title = None

        self.__price = None
        self.__release_date = None
        self.__description = None
        self.__image_url = None
        self.__website_url = None
        self.__genres: list = []
        self.__reviews: list = []
        self.__publisher = None

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    def add_review(self, new_review):
        if not isinstance(new_review, Review) or new_review in self.__reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review):
        if not isinstance(review, Review) or review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def game_id(self):
        return self.__game_id

    @property
    def title(self):
        return self.__game_title

    @title.setter
    def title(self, new_title):
        if type(new_title) is str and new_title.strip() != "":
            self.__game_title = new_title.strip()
        else:
            self.__game_title = None

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price: float):
        if isinstance(price, (int, float)) and price >= 0:
            self.__price = price
        else:
            raise ValueError("Price must be a positive number!")

    @property
    def release_date(self):
        return self.__release_date

    @release_date.setter
    def release_date(self, release_date: str):
        if isinstance(release_date, str):
            try:
                datetime.strptime(release_date, "%b %d, %Y")
                self.__release_date = release_date
            except ValueError:
                raise ValueError("Release date must be in 'Oct 21, 2008' format!")
        else:
            raise ValueError("Release date must be a string in 'Oct 21, 2008' format!")

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str) and description.strip() != "":
            self.__description = description
        else:
            self.__description = None

    @property
    def image_url(self):
        return self.__image_url

    @image_url.setter
    def image_url(self, image_url: str):
        if isinstance(image_url, str) and image_url.strip() != "":
            self.__image_url = image_url
        else:
            self.__image_url = None

    @property
    def website_url(self):
        return self.__website_url

    @website_url.setter
    def website_url(self, website_url: str):
        if isinstance(website_url, str) and website_url.strip() != "":
            self.__website_url = website_url
        else:
            self.__website_url = None

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def genres(self) -> list:
        return sorted(self.__genres, key=lambda x: x.genre_name)

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre) or genre in self.__genres:
            return
        self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return
        try:
            self.__genres.remove(genre)
        except ValueError:
            print(f"Could not find {genre} in list of genres.")
            pass

    def __repr__(self):
        return f"<Game {self.__game_id}, {self.__game_title}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__game_id == other.__game_id

    def __hash__(self):
        return hash(self.__game_id)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__game_id < other.game_id


class User:
    def __init__(self, username: str, password: str):
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError("Username cannot be empty or non-string!")
        else:
            self.__username = username.strip()

        if isinstance(password, str) and len(password) >= 7:
            self.__password = password
        else:
            raise ValueError("Password not valid!")

        self.__reviews: list[Review] = []
        self.__favourite_games: list[Game] = []
        self.__wishlist = Wishlist(self)
        self.__bio = "Write a bio to introduce yourself!"

        #self.__pfp_link

    '''@property
    def pfp_link(self):
        return self.__pfp_link

    @pfp_link.setter
    def pfp_link(self, link: str):
        self.__pfp_link'''

    @property
    def username(self):
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def wishlist(self) -> str:
        return self.__wishlist
    
    @property
    def bio(self):
        return self.__bio

    def add_review(self, new_review):
        if not isinstance(new_review, Review) or new_review in self.__reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review):
        if not isinstance(review, Review) or review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def favourite_games(self) -> list:
        return self.__favourite_games

    def add_favourite_game(self, game):
        if not isinstance(game, Game) or game in self.__favourite_games:
            return
        self.__favourite_games.append(game)

    def remove_favourite_game(self, game):
        if not isinstance(game, Game) or game not in self.__favourite_games:
            return
        self.__favourite_games.remove(game)
    
    def set_bio(self, bio_description):
        self.__bio = bio_description

    def __repr__(self):
        return f"<User {self.__username}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username == other.username

    def __hash__(self):
        return hash(self.__username)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username < other.username


class Review:
    def __init__(self, user: User, game: Game, rating: int, comment: str):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user

        if not isinstance(game, Game):
            raise ValueError("Game must be an instance of Game class")
        self.__game = game

        if not isinstance(rating, int) or not 0 <= rating <= 5:
            raise ValueError("Rating must be an integer between 0 and 5")
        self.__rating = rating

        if not isinstance(comment, str):
            raise ValueError("Comment must be a string")
        self.__comment = comment.strip()

    @property
    def game(self) -> Game:
        return self.__game

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def user(self) -> User:
        return self.__user

    @comment.setter
    def comment(self, new_text):
        if isinstance(new_text, str):
            self.__comment = new_text.strip()
        else:
            raise ValueError("New comment must be a string")

    @rating.setter
    def rating(self, new_rating: int):
        if isinstance(new_rating, int) and 0 <= new_rating <= 5:
            self.__rating = new_rating
        else:
            raise ValueError("Rating must be an integer between 0 and 5")

    def __repr__(self):
        return f"Review(User: {self.__user}, Game: {self.__game}, " f"Rating: {self.__rating}, Comment: {self.__comment})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user == self.__user and other.game == self.__game and other.comment == self.__comment


class Wishlist:
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user

        self.__list_of_games = []
    
    @property
    def list_of_games(self):
        return self.__list_of_games

    def size(self):
        size_wishlist = len(self.__list_of_games)
        if size_wishlist > 0:
            return size_wishlist

    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.__list_of_games:
            self.__list_of_games.append(game)

    def first_game_in_list(self):
        if len(self.__list_of_games) > 0:
            return self.__list_of_games[0]
        else:
            return None

    def remove_game(self, game):
        if isinstance(game, Game) and game in self.__list_of_games:
            self.__list_of_games.remove(game)

    def select_game(self, index):
        if 0 <= index < len(self.__list_of_games):
            return self.__list_of_games[index]
        else:
            return None

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.__current >= len(self.__list_of_games):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_games[self.__current - 1]
