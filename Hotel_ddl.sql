CREATE DATABASE Hotel;
USE Hotel;

CREATE TABLE guests (
    guest_id      INT             NOT NULL AUTO_INCREMENT,
    name          VARCHAR(100)    NOT NULL,
    email         VARCHAR(255)    NOT NULL,
    phone         VARCHAR(20)     NOT NULL,
    PRIMARY KEY (guest_id)
);

CREATE TABLE billings (
    billing_id    INT             NOT NULL AUTO_INCREMENT,
    amount        DECIMAL(12,2)   NOT NULL DEFAULT 0.00,
    billing_date  DATE            NOT NULL,
    PRIMARY KEY (billing_id)
);
CREATE TABLE rooms (
    room_number   INT             NOT NULL AUTO_INCREMENT,
    room_type     VARCHAR(50)     NOT NULL,
    available     BOOLEAN         NOT NULL DEFAULT TRUE,
    rating        DECIMAL(3,2)    NOT NULL DEFAULT 0.00,
    price DECIMAL(10,2)  NOT NULL,
    PRIMARY KEY (room_number)
);


CREATE TABLE services (
    service_id    INT             NOT NULL AUTO_INCREMENT,
    name          VARCHAR(100)    NOT NULL UNIQUE,
    cost DECIMAL(10,2)   NOT NULL DEFAULT 0.00,
    PRIMARY KEY (service_id)
);


CREATE TABLE bookings (
    booking_id    INT             NOT NULL AUTO_INCREMENT,
    guest_id      INT             NOT NULL,
    billing_id    INT             NOT NULL,
    booking_date  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (booking_id),
    FOREIGN KEY (guest_id)   REFERENCES guests(guest_id)
                             ON DELETE CASCADE
                             ON UPDATE CASCADE,
    FOREIGN KEY (billing_id) REFERENCES billings(billing_id)
                             ON DELETE RESTRICT
                             ON UPDATE CASCADE
                             
);

CREATE TABLE booking_room (
    booking_id    INT             NOT NULL,
    room_number   INT             NOT NULL,
    check_in      DATE            NOT NULL,
    check_out     DATE            NOT NULL,
    PRIMARY KEY (booking_id, room_number),
    FOREIGN KEY (booking_id)  REFERENCES bookings(booking_id)
                              ON DELETE CASCADE
                              ON UPDATE CASCADE,
    FOREIGN KEY (room_number) REFERENCES rooms(room_number)
                              ON DELETE RESTRICT
                              ON UPDATE CASCADE
                              
);

CREATE TABLE booking_service (	
    booking_id    INT             NOT NULL,
    service_id    INT             NOT NULL,
    quantity      INT             NOT NULL DEFAULT 1,
    unit_cost     DECIMAL(10,2)   NOT NULL,
    PRIMARY KEY (booking_id, service_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
								ON DELETE CASCADE
                                ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id)
                              ON DELETE RESTRICT
                               ON UPDATE CASCADE
);
