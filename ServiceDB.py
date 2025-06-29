import DB

def get_service_by_id(db :DB,service_id: int):
    db.cursor.execute("SELECT * FROM services WHERE service_id=%s", (service_id,))
    return db.cursor.fetchone()

def get_all_services(db :DB):
    db.cursor.execute("SELECT name,cost FROM services")
    return db.cursor.fetchall()

def service_exists(db :DB,service_id: int):
    db.cursor.execute("SELECT service_id FROM services WHERE service_id=%s", (service_id,))
    result = db.cursor.fetchone()
    return result[0] if result else None

def get_service_by_name(db :DB,name: str):
    db.cursor.execute("SELECT service_id FROM services WHERE name=%s", (name,))
    return db.cursor.fetchone()

def get_service_price(db :DB,service_id: int):
    db.cursor.execute("SELECT cost FROM services WHERE service_id=%s", (service_id,))
    result = db.cursor.fetchone()
    return result[0] if result else None

def add_service(db :DB,name, cost):
    db.cursor.execute("Insert Into services (name,cost) VALUES (%s, %s)",
                        (name, cost))
    db.connection.commit()
