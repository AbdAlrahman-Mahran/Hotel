from datetime import datetime

import DB
import GuestDB
import RoomDB
import ServiceDB
import BookingDB
from Guest import Guest
from Room import Room

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox

date_format ="%Y-%m-%d"
db = DB.DB("localhost", "root", "yami", "Hotel")
ctk.set_appearance_mode("Dark")

class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hotel Management System")
        self.geometry("1024x768")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.pages = {}
        for P in (
        HomePage, BookingPage, GuestsPage, BillingPage, RoomsPage, RoomDetailsPage, PriceFilterPage, RatingFilterPage,
        ServicesPage,UserHomePage,AdminHomePage,AddRoomPage,AddGuestPage,AddServicePage,GuestBillingDetailsPage,
        ShowGuestsPage,GuestDetailsByNamePage,ShowAvailableRoomsPage,RoomBookingPage,ServiceBookingPage,GuestBookingsPage):
            page = P(parent=self.container, controller=self)
            self.pages[P.__name__] = page
            page.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        self.show_page("HomePage")

    def show_page(self, page_name):
        self.pages[page_name].lift()



class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Hotel Management System", font=("Arial", 22)).pack(pady=40)
        ctk.CTkButton(self, text="User View", command=lambda: controller.show_page("UserHomePage")).pack(pady=20)
        ctk.CTkButton(self, text="Admin View", command=lambda: controller.show_page("AdminHomePage")).pack(pady=20)


class UserHomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Welcome to Hotel Management System", font=("Arial", 20)).pack(pady=20)
        ctk.CTkButton(self, text="Booking", command=lambda: controller.show_page("BookingPage")).pack(pady=20)
        ctk.CTkButton(self, text="Guests", command=lambda: controller.show_page("GuestsPage")).pack(pady=20)
        ctk.CTkButton(self, text="Billing", command=lambda: controller.show_page("BillingPage")).pack(pady=20)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("HomePage")).pack(pady=20)



class AdminHomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Admin View", font=("Arial", 20)).pack(pady=40)
        ctk.CTkButton(self, text="Add Room", command=lambda: controller.show_page("AddRoomPage")).pack(pady=20)
        ctk.CTkButton(self, text="Add Guest", command=lambda: controller.show_page("AddGuestPage")).pack(pady=20)
        ctk.CTkButton(self, text="Add Service", command=lambda: controller.show_page("AddServicePage")).pack(pady=20)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("HomePage")).pack(pady=20)




class AddRoomPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Add Room", font=("Arial", 18)).pack(pady=10)

        room_number_frame = ctk.CTkFrame(self)
        room_number_frame.pack(pady=5)
        room_number_label = ctk.CTkLabel(room_number_frame, text="Room Number", width=100, anchor="w")
        room_number_label.pack(side="left", padx=(0, 10))
        self.room_number_entry = ctk.CTkEntry(room_number_frame, width=250)
        self.room_number_entry.pack(side="left")

        room_type_frame = ctk.CTkFrame(self)
        room_type_frame.pack(pady=5)
        room_type_label = ctk.CTkLabel(room_type_frame, text="Room Type", width=100, anchor="w")
        room_type_label.pack(side="left", padx=(0, 10))
        self.room_type_entry = ctk.CTkEntry(room_type_frame, width=250)
        self.room_type_entry.pack(side="left")

        room_rating_frame = ctk.CTkFrame(self)
        room_rating_frame.pack(pady=5)
        room_rating_label = ctk.CTkLabel(room_rating_frame, text="Room Rating", width=100, anchor="w")
        room_rating_label.pack(side="left", padx=(0, 10))
        self.room_rating_entry = ctk.CTkEntry(room_rating_frame, width=250)
        self.room_rating_entry.pack(side="left")

        price_frame = ctk.CTkFrame(self)
        price_frame.pack(pady=5)
        price_label = ctk.CTkLabel(price_frame, text="Price", width=100, anchor="w")
        price_label.pack(side="left", padx=(0, 10))
        self.price_entry = ctk.CTkEntry(price_frame, width=250)
        self.price_entry.pack(side="left")

        ctk.CTkButton(self, text="Submit", command=self.submit_room).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("AdminHomePage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.room_number_entry.delete(0, "end")
        self.room_type_entry.delete(0, "end")
        self.room_rating_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        super().lift(*args, **kwargs)

    def submit_room(self):
        room_number = self.room_number_entry.get()
        room_type = self.room_type_entry.get()
        room_rating = self.room_rating_entry.get()
        price = self.price_entry.get()
        if not room_number or not room_type or not room_rating or not price:
            messagebox.showerror("Input Error", "All fields are required!")
            return
        try:
            room = Room(room_type, True, float(room_rating), float(price), int(room_number))
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return

        if RoomDB.room_exists(db, int(room_number)):
            messagebox.showerror("Input Error", f"Room {room_number} already exists!")
            return

        RoomDB.add_room(db, room)
        messagebox.showinfo("Room Added", f"Room {room_number} added successfully!")
        self.controller.show_page("AdminHomePage")


class AddGuestPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Add Guest", font=("Arial", 18)).pack(pady=10)

        name_frame = ctk.CTkFrame(self)
        name_frame.pack(pady=5)
        name_label = ctk.CTkLabel(name_frame, text="Name", width=100, anchor="w")
        name_label.pack(side="left", padx=(0, 10))
        self.name_entry = ctk.CTkEntry(name_frame, width=250)
        self.name_entry.pack(side="left")

        phone_frame = ctk.CTkFrame(self)
        phone_frame.pack(pady=5)
        phone_label = ctk.CTkLabel(phone_frame, text="Phone", width=100, anchor="w")
        phone_label.pack(side="left", padx=(0, 10))
        self.phone_entry = ctk.CTkEntry(phone_frame, width=250)
        self.phone_entry.pack(side="left")

        email_frame = ctk.CTkFrame(self)
        email_frame.pack(pady=5)
        email_label = ctk.CTkLabel(email_frame, text="Email", width=100, anchor="w")
        email_label.pack(side="left", padx=(0, 10))
        self.email_entry = ctk.CTkEntry(email_frame, width=250)
        self.email_entry.pack(side="left")

        ctk.CTkButton(self, text="Submit", command=self.submit_guest).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("AdminHomePage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        super().lift(*args, **kwargs)

    def submit_guest(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        if not name or not phone or not email:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            guest = Guest(name, email, phone)
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return
        GuestDB.add_guest(db, guest)
        messagebox.showinfo("Guest Added", f"Guest {name} added successfully!")
        self.controller.show_page("AdminHomePage")


class AddServicePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Add Service", font=("Arial", 18)).pack(pady=10)

        service_name_frame = ctk.CTkFrame(self)
        service_name_frame.pack(pady=5)
        service_name_label = ctk.CTkLabel(service_name_frame, text="Service Name", width=100, anchor="w")
        service_name_label.pack(side="left", padx=(0, 10))
        self.service_name_entry = ctk.CTkEntry(service_name_frame, width=250)
        self.service_name_entry.pack(side="left")

        price_frame = ctk.CTkFrame(self)
        price_frame.pack(pady=5)
        price_label = ctk.CTkLabel(price_frame, text="Price", width=100, anchor="w")
        price_label.pack(side="left", padx=(0, 10))
        self.price_entry = ctk.CTkEntry(price_frame, width=250)
        self.price_entry.pack(side="left")

        ctk.CTkButton(self, text="Submit", command=self.submit_service).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("AdminHomePage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.service_name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        super().lift(*args, **kwargs)

    def submit_service(self):
        service_name = self.service_name_entry.get()
        price = self.price_entry.get()
        if not service_name or not price:
            messagebox.showerror("Input Error", "All fields are required!")
            return
        try:
            ServiceDB.add_service(db, service_name, float(price))
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return
        messagebox.showinfo("Service Added", f"Service {service_name} added successfully!")
        self.controller.show_page("AdminHomePage")


class BookingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Booking Page", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Book a Room", command=lambda: controller.show_page("RoomBookingPage")).pack(pady=20)
        ctk.CTkButton(self, text="Book a Service", command=lambda: controller.show_page("ServiceBookingPage")).pack(pady=20)
        ctk.CTkButton(self, text="Rooms", command=lambda: controller.show_page("RoomsPage")).pack(pady=20)
        ctk.CTkButton(self, text="Services", command=lambda: controller.show_page("ServicesPage")).pack(pady=20)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("UserHomePage")).pack(pady=20)


class RoomBookingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Book a Room", font=("Arial", 18)).pack(pady=10)

        guest_frame = ctk.CTkFrame(self)
        guest_frame.pack(pady=5)
        guest_label = ctk.CTkLabel(guest_frame, text="Guest_ID", width=180, anchor="w")
        guest_label.pack(side="left", padx=(0, 10))
        self.guest_entry = ctk.CTkEntry(guest_frame, width=250)
        self.guest_entry.pack(side="left")

        room_frame = ctk.CTkFrame(self)
        room_frame.pack(pady=5)
        room_label = ctk.CTkLabel(room_frame, text="Room Number", width=180, anchor="w")
        room_label.pack(side="left", padx=(0, 10))
        self.room_number_entry = ctk.CTkEntry(room_frame, width=250)
        self.room_number_entry.pack(side="left")

        checkin_frame = ctk.CTkFrame(self)
        checkin_frame.pack(pady=5)
        checkin_label = ctk.CTkLabel(checkin_frame, text="Check-in Date (YYYY-MM-DD)", width=180, anchor="w")
        checkin_label.pack(side="left", padx=(0, 10))
        self.check_in_entry = ctk.CTkEntry(checkin_frame, width=250)
        self.check_in_entry.pack(side="left")

        checkout_frame = ctk.CTkFrame(self)
        checkout_frame.pack(pady=5)
        checkout_label = ctk.CTkLabel(checkout_frame, text="Check-out Date (YYYY-MM-DD)", width=180, anchor="w")
        checkout_label.pack(side="left", padx=(0, 10))
        self.check_out_entry = ctk.CTkEntry(checkout_frame, width=250)
        self.check_out_entry.pack(side="left")

        bookingid_frame = ctk.CTkFrame(self)
        bookingid_frame.pack(pady=5)
        bookingid_label = ctk.CTkLabel(bookingid_frame, text="Booking_ID (-1 if None)", width=180, anchor="w")
        bookingid_label.pack(side="left", padx=(0, 10))
        self.booking_entry = ctk.CTkEntry(bookingid_frame, width=250)
        self.booking_entry.pack(side="left")

        ctk.CTkButton(self, text="Submit", command=self.book_room).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("BookingPage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.guest_entry.delete(0, "end")
        self.room_number_entry.delete(0, "end")
        self.check_in_entry.delete(0, "end")
        self.check_out_entry.delete(0, "end")
        self.booking_entry.delete(0, "end")
        super().lift(*args, **kwargs)

    def book_room(self):
        guest_id = self.guest_entry.get()
        room_number = self.room_number_entry.get()
        check_in = datetime.strptime(self.check_in_entry.get(), date_format)
        check_out = datetime.strptime(self.check_out_entry.get(), date_format)
        booking_id = self.booking_entry.get()

        if not GuestDB.guest_exists(db, guest_id):
            messagebox.showerror("Booking Error", f"Guest {guest_id} does not exist.")
            return
        if not RoomDB.room_exists(db, room_number):
            messagebox.showerror("Booking Error", f"Room {room_number} does not exist.")
            return
        bookings = BookingDB.get_bookings_for_room(db, room_number)
        for booking in bookings:
            if booking[0] <= check_in <= booking[1] or booking[0] <= check_out <= booking[1]:
                messagebox.showerror("Booking Error", f"Room {room_number} is already booked during this period.")
                return

        if int(booking_id) == -1:
            booking_id = BookingDB.add_booking(db, guest_id, check_in, check_out)
        BookingDB.book_room(db, room_number, booking_id, check_in, check_out)
        messagebox.showinfo("Booking", f"Room {room_number} booked from {check_in} to {check_out}")

class ServiceBookingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Book a Service", font=("Arial", 18)).pack(pady=10)

        booking_id_frame = ctk.CTkFrame(self)
        booking_id_frame.pack(pady=5)
        booking_id_label = ctk.CTkLabel(booking_id_frame, text="Booking ID", width=100, anchor="w")
        booking_id_label.pack(side="left", padx=(0, 10))
        self.booking_id_entry = ctk.CTkEntry(booking_id_frame, width=250)
        self.booking_id_entry.pack(side="left")

        service_name_frame = ctk.CTkFrame(self)
        service_name_frame.pack(pady=5)
        service_name_label = ctk.CTkLabel(service_name_frame, text="Service Name", width=100, anchor="w")
        service_name_label.pack(side="left", padx=(0, 10))
        self.service_name_entry = ctk.CTkEntry(service_name_frame, width=250)
        self.service_name_entry.pack(side="left")

        quantity_frame = ctk.CTkFrame(self)
        quantity_frame.pack(pady=5)
        quantity_label = ctk.CTkLabel(quantity_frame, text="Quantity", width=100, anchor="w")
        quantity_label.pack(side="left", padx=(0, 10))
        self.quantity_entry = ctk.CTkEntry(quantity_frame, width=250)
        self.quantity_entry.pack(side="left")

        ctk.CTkButton(self, text="Submit", command=self.book_service).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("BookingPage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.booking_id_entry.delete(0, "end")
        self.service_name_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        super().lift(*args, **kwargs)

    def book_service(self):
        booking_id = self.booking_id_entry.get()
        service_name = self.service_name_entry.get()
        quantity = self.quantity_entry.get()

        if not booking_id or not service_name or not quantity:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            booking_id = int(booking_id)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Input Error", "Booking ID and Quantity must be integers.")
            return

        if not BookingDB.booking_exists(db, booking_id):
            messagebox.showerror("Booking Error", f"Booking ID {booking_id} does not exist.")
            return

        if not ServiceDB.service_exists(db, service_name):
            messagebox.showerror("Service Error", f"Service '{service_name}' does not exist.")
            return

        try:
            BookingDB.book_service(db, booking_id, service_name, quantity)
            messagebox.showinfo("Success", f"Service '{service_name}' booked for Booking ID {booking_id}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book service: {e}")

class ServicesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Hotel Services", font=("Arial", 18)).pack(pady=10)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=300)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkButton(self, text="Back to Booking", command=lambda: controller.show_page("BookingPage")).pack(pady=10)

    def lift(self, *args, **kwargs):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        services = ServiceDB.get_all_services(db)
        for service in services:
            ctk.CTkLabel(
                self.scroll_frame,
                text=f"{service[0]} costs {float(service[1])}$",
                anchor="w",
                font=("Arial", 14)
            ).pack(fill="x", pady=2, padx=10)
        super().lift(*args, **kwargs)

class RoomsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Rooms Page", font=("Arial", 18)).pack(pady=15)
        ctk.CTkButton(self, text="List Available Rooms",command=lambda: controller.show_page("ShowAvailableRoomsPage")).pack(pady=10)
        ctk.CTkButton(self, text="List Rooms by Rating", command=lambda: controller.show_page("RatingFilterPage")).pack(pady=10)
        ctk.CTkButton(self, text="List Rooms by Price", command=lambda: controller.show_page("PriceFilterPage")).pack(pady=10)
        ctk.CTkButton(self, text="Get Room Details", command=lambda: controller.show_page("RoomDetailsPage")).pack(pady=10)
        ctk.CTkButton(self, text="Back to Booking", command=lambda: controller.show_page("BookingPage")).pack(pady=15)
        self.result_label = ctk.CTkLabel(self, text="", wraplength=600, justify="left")
        self.result_label.pack(pady=10)


class ShowAvailableRoomsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Available Rooms", font=("Arial", 18)).pack(pady=10)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("RoomsPage")).pack(pady=10)

    def lift(self, *args, **kwargs):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        rooms = RoomDB.get_available_rooms(db)
        if not rooms:
            ctk.CTkLabel(self.scroll_frame, text="No available rooms.", font=("Arial", 14)).pack(pady=5)
        else:
            for room in rooms:
                room_frame = ctk.CTkFrame(self.scroll_frame)
                room_frame.pack(fill="x", pady=2)
                room.display_colored(room_frame)
        super().lift(*args, **kwargs)


class RoomDetailsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Enter Room Number", font=("Arial", 16)).pack(pady=10)
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=5)
        entry_label = ctk.CTkLabel(entry_frame, text="Room number", width=120, anchor="w")
        entry_label.pack(side="left", padx=(0, 10))
        self.entry = ctk.CTkEntry(entry_frame, width=250)
        self.entry.pack(side="left")
        self.result_label = ctk.CTkLabel(self, text="", wraplength=600, justify="left")
        self.result_label.pack(pady=10)
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(pady=10, fill="x", expand=True)
        ctk.CTkButton(self, text="Submit", command=self.show_details).pack(pady=5)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("RoomsPage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.entry.delete(0, "end")
        self.result_label.configure(text="")
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        super().lift(*args, **kwargs)

    def show_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.result_label.configure(text="")

        room_no = self.entry.get()
        try:
            room_no_int = int(room_no)
        except ValueError:
            self.result_label.configure(text="Please enter a valid room number.")
            return

        if not RoomDB.room_exists(db, room_no_int):
            self.result_label.configure(text="Room does not exist.")
            return

        room_gen = RoomDB.get_room(db, room_no_int)
        room = next(room_gen, None)
        if room is None:
            self.result_label.configure(text="Room does not exist.")
            return
        room.display_colored(self.details_frame)


class PriceFilterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Enter Maximum Price", font=("Arial", 16)).pack(pady=10)
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=5)
        entry_label = ctk.CTkLabel(entry_frame, text="Maximum price", width=120, anchor="w")
        entry_label.pack(side="left", padx=(0, 10))
        self.entry = ctk.CTkEntry(entry_frame, width=250)
        self.entry.pack(side="left")
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=300)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkButton(self, text="Submit", command=self.show_results).pack(pady=5)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("RoomsPage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.entry.delete(0, "end")
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        super().lift(*args, **kwargs)

    def show_results(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        try:
            max_price = float(self.entry.get())
        except ValueError:
            ctk.CTkLabel(self.scroll_frame, text="Please enter a valid price").pack(pady=5)
            return

        rooms = RoomDB.get_room_by_price(db, max_price)
        if not rooms:
            ctk.CTkLabel(self.scroll_frame, text="No rooms found for this price.").pack(pady=5)
            return
        for room in rooms:
            room_frame = ctk.CTkFrame(self.scroll_frame)
            room_frame.pack(fill="x", pady=2)
            room.display_colored(room_frame)


class RatingFilterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Enter Minimum Rating", font=("Arial", 16)).pack(pady=10)
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=5)
        entry_label = ctk.CTkLabel(entry_frame, text="Minimum rating", width=120, anchor="w")
        entry_label.pack(side="left", padx=(0, 10))
        self.entry = ctk.CTkEntry(entry_frame, width=250)
        self.entry.pack(side="left")
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=300)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkButton(self, text="Submit", command=self.show_results).pack(pady=5)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("RoomsPage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.entry.delete(0, "end")
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        super().lift(*args, **kwargs)

    def show_results(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        try:
            min_rating = float(self.entry.get())
        except ValueError:
            ctk.CTkLabel(self.scroll_frame, text="Please enter a valid rating").pack(pady=5)
            return

        rooms = RoomDB.get_room_by_rating(db, min_rating)
        if not rooms:
            ctk.CTkLabel(self.scroll_frame, text="No rooms found for this rating.").pack(pady=5)
            return
        for room in rooms:
            room_frame = ctk.CTkFrame(self.scroll_frame)
            room_frame.pack(fill="x", pady=2)
            room.display_colored(room_frame)

class GuestsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Guests Page", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Show Current Guests", command=lambda: controller.show_page("ShowGuestsPage")).pack(pady=10)
        ctk.CTkButton(self, text="Find Guest by Name", command=lambda: controller.show_page("GuestDetailsByNamePage")).pack(pady=10)
        ctk.CTkButton(self, text="Show Guest Bookings", command=lambda: controller.show_page("GuestBookingsPage")).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("UserHomePage")).pack(pady=10)
        self.result_label = ctk.CTkLabel(self, text="", wraplength=600, justify="left")
        self.result_label.pack(pady=10)


class GuestBookingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Enter Guest_ID to Show Bookings", font=("Arial", 16)).pack(pady=10)
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=5)
        entry_label = ctk.CTkLabel(entry_frame, text="Guest_ID", width=120, anchor="w")
        entry_label.pack(side="left", padx=(0, 10))
        self.entry = ctk.CTkEntry(entry_frame, width=250)
        self.entry.pack(side="left")
        ctk.CTkButton(self, text="Show Bookings", command=self.show_bookings).pack(pady=5)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("GuestsPage")).pack(pady=5)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=300)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def lift(self, *args, **kwargs):
        self.entry.delete(0, "end")
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        super().lift(*args, **kwargs)

    def show_bookings(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        guest_id = self.entry.get()
        try:
            bookings = BookingDB.get_bookings_by_guest(db, int(guest_id))
        except Exception:
            ctk.CTkLabel(self.scroll_frame, text="Invalid Guest_ID").pack(pady=5)
            return

        if not bookings:
            ctk.CTkLabel(self.scroll_frame, text="No bookings found for this guest").pack(pady=5)
            return

        for booking in bookings:
            rooms = BookingDB.get_rooms_by_booking(db, booking[0])
            ctk.CTkLabel(
                self.scroll_frame,
                text=f"Rooms for booking_id = {booking[0]} :-",
                anchor="w",
                text_color="#00BFFF"  # Blue
            ).pack(fill="x", pady=2, padx=10)
            for room in rooms:
                ctk.CTkLabel(
                    self.scroll_frame,
                    text=f"Room Number: {room[0]}, Check-in: {room[1]}, Check-out: {room[2]}",
                    anchor="w",
                    text_color="#32CD32"  # Green
                ).pack(fill="x", pady=2, padx=10)


class ShowGuestsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Current Guests", font=("Arial", 18)).pack(pady=10)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("GuestsPage")).pack(pady=10)

    def lift(self, *args, **kwargs):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        guests = GuestDB.get_all_guests(db)
        if not guests:
            ctk.CTkLabel(self.scroll_frame, text="No guests found.", font=("Arial", 14)).pack(pady=5)
        else:
            for g in guests:
                guest_frame = ctk.CTkFrame(self.scroll_frame)
                guest_frame.pack(fill="x", pady=2)
                g.display_colored(guest_frame)
        super().lift(*args, **kwargs)

class GuestDetailsByNamePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Enter Guest Name", font=("Arial", 16)).pack(pady=10)
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=5)
        entry_label = ctk.CTkLabel(entry_frame, text="Guest Name", width=120, anchor="w")
        entry_label.pack(side="left", padx=(0, 10))
        self.entry = ctk.CTkEntry(entry_frame, width=250)
        self.entry.pack(side="left")
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=300)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkButton(self, text="Submit", command=self.show_details).pack(pady=5)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("GuestsPage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.entry.delete(0, "end")
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        super().lift(*args, **kwargs)

    def show_details(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        guest_name = self.entry.get()
        guests = GuestDB.get_guests_by_name(db, guest_name)
        if not guests:
            ctk.CTkLabel(self.scroll_frame, text="No guest found with that name.").pack(pady=5)
            return
        for g in guests:
            guest_frame = ctk.CTkFrame(self.scroll_frame)
            guest_frame.pack(fill="x", pady=2)
            g.display_colored(guest_frame)

class BillingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Billing Page", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Guest Billing Details", command=lambda: controller.show_page("GuestBillingDetailsPage")).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("UserHomePage")).pack(pady=10)

class GuestBillingDetailsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Enter Guest_ID", font=("Arial", 16)).pack(pady=10)
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=5)
        entry_label = ctk.CTkLabel(entry_frame, text="Guest_ID", width=120, anchor="w")
        entry_label.pack(side="left", padx=(0, 10))
        self.entry = ctk.CTkEntry(entry_frame, width=250)
        self.entry.pack(side="left")
        self.result_label = ctk.CTkLabel(self, text="", wraplength=900, justify="left")
        self.result_label.pack(pady=10)
        ctk.CTkButton(self, text="Submit", command=self.show_details).pack(pady=5)
        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("BillingPage")).pack(pady=5)

    def lift(self, *args, **kwargs):
        self.entry.delete(0, "end")
        self.result_label.configure(text="")
        super().lift(*args, **kwargs)

    def show_details(self):
        guest_id = self.entry.get()
        try:
            bookings = BookingDB.get_bookings_by_guest(db, int(guest_id))
        except Exception:
            self.result_label.configure(text="Invalid Guest_ID")
            return
        if not bookings:
            self.result_label.configure(text="No bookings found for this guest")
            return
        for booking in bookings:
            billing_id = BookingDB.get_billing_id(db, booking[0])
            billing_details = BookingDB.get_billing_details(db, billing_id)
            if billing_details:
                #self.result_label.pack_forget()

                self.result_label = ctk.CTkTextbox(self, width=900, height=100, font=("Arial", 16, "bold"))
                self.result_label.pack(pady=10)
                self.result_label.insert("end", f"Billing details for Guest_ID {guest_id}:\n", "header")
                self.result_label.insert("end",
                                         f"- and Booking_ID {booking[0]}:- Amount: ${(float(billing_details[0]))}\n",
                                         "amount")
                self.result_label.insert("end", f"-Billing Date: {billing_details[1]}", "date")
                self.result_label.tag_config("header", foreground="#00BFFF")
                self.result_label.tag_config("amount", foreground="#32CD32")
                self.result_label.tag_config("date", foreground="#FFD700")
                self.result_label.configure(state="disabled")
        return


app = HotelApp()
app.mainloop()
