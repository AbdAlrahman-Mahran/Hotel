import customtkinter as ctk
class Guest:
    def __init__(self,name, email, phone,guest_id=None):
        self.guest_id = guest_id
        self.name = name
        self.email = email
        self.phone = phone

    def display_colored(self, parent):
        ctk.CTkLabel(parent, text="Guest Name:", text_color="#00BCD4").pack(side="left")
        ctk.CTkLabel(parent, text=self.name, text_color="#FFEB3B").pack(side="left")
        ctk.CTkLabel(parent, text=" | Guest ID:", text_color="#00BCD4").pack(side="left")
        ctk.CTkLabel(parent, text=str(self.guest_id), text_color="#4CAF50").pack(side="left")
        ctk.CTkLabel(parent, text=" | Email:", text_color="#00BCD4").pack(side="left")
        ctk.CTkLabel(parent, text=self.email, text_color="#E040FB").pack(side="left")
        ctk.CTkLabel(parent, text=" | Phone:", text_color="#00BCD4").pack(side="left")
        ctk.CTkLabel(parent, text=self.phone, text_color="#FFEB3B").pack(side="left")

