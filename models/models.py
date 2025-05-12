from dataclasses import dataclass

@dataclass
class Ticket:
    name: str
    row: str
    seat: str
    movie: str
    session: str

def ticket_from_dict(data: dict) -> Ticket:
    return Ticket(
        name=data.get("name", "-"),
        row=data.get("row", "-"),
        seat=data.get("seat", "-"),
        movie=data.get("movie", "-"),
        session=data.get("session", "-")
    )

def ticket_to_dict(ticket: Ticket) -> dict:
    return {
        "name": ticket.name,
        "row": ticket.row,
        "seat": ticket.seat,
        "movie": ticket.movie,
        "session": ticket.session
    }

@dataclass
class Viewer:
    def __init__(self, name, row, seat, movie, session):
        self.name = name
        self.row = row
        self.seat = seat
        self.movie = movie
        self.session = session

    def __str__(self):
        return (f"Ім’я: {self.name} | Фільм: {self.movie} | Сеанс: {self.session} | "
                f"Ряд: {self.row} | Місце: {self.seat}")

@dataclass
class Manager:
    def __init__(self, name, gender, birthdate, phone, email, extra_info=""):
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.phone = phone
        self.email = email
        self.extra_info = extra_info

    def __str__(self):
        return f"{self.name} ({self.email})"

@dataclass
class Movie:
    title: str

    def __str__(self):
        return self.title

@dataclass
class Session:
    description: str

    def __str__(self):
        return self.description


