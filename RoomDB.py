import DB
import Room

def get_room(db :DB,room_number: int):
    db.cursor.execute("SELECT * FROM rooms WHERE room_number=%s", (room_number,))
    room = db.cursor.fetchone()
    yield Room.Room(room[1], room[2], room[3], room[4],room[0] )

def room_exists(db :DB,room_number: int):
    db.cursor.execute("SELECT room_number FROM rooms WHERE room_number=%s", (room_number,))
    result = db.cursor.fetchone()
    return result[0] if result else None

def get_available_rooms(db :DB):
    db.cursor.execute("SELECT * FROM rooms WHERE available=1")
    for room in db.cursor.fetchall():
        yield Room.Room(room[1], room[2], room[3], room[4],room[0] )


def is_available(db :DB,room_number: int):
    db.cursor.execute("SELECT available FROM rooms WHERE room_number=%s", (room_number,))
    result = db.cursor.fetchone()
    return result[0] if result else None


def get_room_by_rating(db :DB,rating: float):
    db.cursor.execute("SELECT * FROM rooms WHERE rating>=%s", (rating,))
    for room in db.cursor.fetchall():
        yield Room.Room(room[1], room[2], room[3], room[4],room[0] )


def get_room_by_price(db :DB,price: float):
    db.cursor.execute("SELECT * FROM rooms WHERE price<=%s", (price,))
    for room in db.cursor.fetchall():
        yield Room.Room(room[1], room[2], room[3], room[4],room[0] )

def get_room_price(db :DB,room_number: int):
    db.cursor.execute("SELECT price FROM rooms WHERE room_number=%s", (room_number,))
    result = db.cursor.fetchone()
    return result[0] if result else None

def add_room(db :DB,room : Room):
    if room_exists(db,room.room_number):
        return
    db.cursor.execute("INSERT INTO rooms (room_number,room_type, price, rating) VALUES (%s,%s, %s, %s)",
                        (room.room_number,room.room_type, room.price, room.rating))
    db.connection.commit()


