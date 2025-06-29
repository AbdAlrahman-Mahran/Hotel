import DB
import RoomDB
import ServiceDB

def get_booking_by_id(db :DB,booking_id: int):
    if booking_id < 0:
        db.cursor.execute("SELECT * FROM bookings")
    else:
        db.cursor.execute("SELECT * FROM bookings WHERE booking_id=%s", (booking_id,))
    return db.cursor.fetchall()


def get_bookings_by_guest(db :DB,guest_id: int):
    db.cursor.execute("SELECT * FROM bookings WHERE guest_id=%s", (guest_id,))
    return db.cursor.fetchall()

def booking_exists(db :DB,booking_id: int):
    db.cursor.execute("SELECT booking_id FROM bookings WHERE booking_id=%s", (booking_id,))
    result = db.cursor.fetchone()
    return result[0] if result else None

def get_billing_id(db :DB,booking_id: int):
    db.cursor.execute("SELECT billing_id FROM bookings WHERE booking_id=%s", (booking_id,))
    result = db.cursor.fetchone()
    return result[0] if result else None

def get_billing_details(db :DB, billing_id: int):
    db.cursor.execute("SELECT amount,billing_date FROM billings WHERE billing_id=%s", (billing_id,))
    return db.cursor.fetchone()

def add_booking(db :DB,guest_id, check_in, check_out):
    db.cursor.execute("INSERT INTO billings (amount,billing_date) VALUES (%s, %s)", (0.0, check_in))
    billing_id = db.cursor.lastrowid
    db.connection.commit()
    db.cursor.execute("INSERT INTO bookings (guest_id, billing_id, booking_date) VALUES (%s, %s, %s)",
                        (guest_id, billing_id, check_in))
    booking_id = db.cursor.lastrowid
    db.connection.commit()
    return booking_id


def book_room(db :DB,room_number, booking_id, check_in_date, check_out_date):
    db.cursor.execute(
        "INSERT INTO booking_room (room_number, booking_id,check_in,check_out) VALUES (%s, %s, %s, %s)",
         (room_number, booking_id, check_in_date, check_out_date))

    billing_id = get_billing_id(db,booking_id)
    price = RoomDB.get_room_price(db,room_number)
    cost = price * (check_out_date - check_in_date).days

    db.cursor.execute("UPDATE billings SET amount=amount+%s WHERE billing_id=%s", (cost, billing_id))
    db.connection.commit()

def get_rooms_by_booking(db :DB, booking_id: int):
    db.cursor.execute("SELECT room_number,check_in,check_out FROM booking_room WHERE booking_id=%s", (booking_id,))
    return db.cursor.fetchall()

def get_bookings_for_room(db :DB, room_number: int):
    db.cursor.execute("SELECT check_in, check_out FROM booking_room WHERE room_number=%s", (room_number,))
    return db.cursor.fetchall()

def book_service(db :DB,service_id, booking_id,quantity):
    unit_cost= ServiceDB.get_service_price(db,service_id)

    db.cursor.execute(
        "INSERT INTO booking_service (service_id, booking_id, unit_cost,quantity) VALUES (%s, %s, %s, %s)",
         (service_id, booking_id,unit_cost,quantity))

    billing_id = get_billing_id(db,booking_id)
    cost = unit_cost * quantity

    db.cursor.execute("UPDATE billings SET amount=amount+%s WHERE billing_id=%s", (cost, billing_id))
    db.connection.commit()