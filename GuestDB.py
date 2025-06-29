import DB
import Guest


def get_guest_by_id(db :DB,guest_id: int):
    db.cursor.execute("SELECT * FROM guests WHERE guest_id=%s", (guest_id,))
    guest = db.cursor.fetchone()
    yield Guest.Guest( guest[1], guest[2], guest[3],guest[0]) if guest else None

def get_all_guests(db :DB):
    db.cursor.execute("SELECT * FROM guests")
    for guest in db.cursor.fetchall():
        yield Guest.Guest( guest[1], guest[2], guest[3],guest[0])

def get_guests_by_name(db :DB,name: str):
    db.cursor.execute("SELECT * FROM guests WHERE name=%s", (name,))
    for guest in db.cursor.fetchall():
        yield Guest.Guest( guest[1], guest[2], guest[3],guest[0])

def guest_exists(db :DB,guest_id: int):
    db.cursor.execute("SELECT guest_id FROM guests WHERE guest_id=%s", (guest_id,))
    result = db.cursor.fetchone()
    return result[0] if result else None

def add_guest(db :DB,guest :Guest):
    db.cursor.execute("Insert Into guests (name,email,phone) VALUES (%s, %s, %s)",
                        (guest.name, guest.email, guest.phone))
    db.connection.commit()
