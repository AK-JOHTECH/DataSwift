import Login
import tkinter as tk
import customtkinter # <- import the CustomTkinter module



#===============Main=============================================
if __name__ == "__main__":
    global root
    root = customtkinter.CTk()
    root.withdraw()
    Login.login_system()
    root.mainloop()

