import customtkinter as ctk
class Room:
    def __init__(self, room_type,available,rating, price,room_number = None):
        self.room_number = room_number
        self.room_type = room_type
        self.available = available
        self.rating = rating
        self.price = price

    def display_colored(self, parent):
        ctk.CTkLabel(parent, text="Room Number:", text_color="#00BCD4").pack(side="left")
        ctk.CTkLabel(parent, text=str(self.room_number), text_color="#FFEB3B").pack(side="left")
        ctk.CTkLabel(parent, text=" | Room Type:", text_color="#00BCD4").pack(side="left")
        ctk.CTkLabel(parent, text=self.room_type, text_color="#4CAF50").pack(side="left")
        ctk.CTkLabel(parent, text=" | Rating:", text_color="#00BCD4").pack(side="left")
        ctk.CTkLabel(parent, text=str(self.rating), text_color="#E040FB").pack(side="left")
        ctk.CTkLabel(parent, text=" | Price:", text_color="#00BCD4").pack(side="left")
        ctk.CTkLabel(parent, text=str(self.price), text_color="#FFEB3B").pack(side="left")
