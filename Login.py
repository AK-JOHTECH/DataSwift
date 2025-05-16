import CTKlib
import access as acc
import Drill_Form
import Fired_Form
from tkinter import TclError
import re
import Access_Page
import time
import tkinter as tk
import customtkinter # <- import the CustomTkinter module
#==================Sign  up system================================
def sign_up_menu():
    global login_root
    login_root.withdraw()
    signup_root = CTKlib.Window()
    signup_root.title('IT Log In')
    signup_root.geometry('300x450')

    username_su = customtkinter.CTkEntry(signup_root,placeholder_text ='Username',corner_radius= 80)
    username_su.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    password_su = customtkinter.CTkEntry(signup_root,placeholder_text = 'Password',corner_radius = 80, show='•')
    password_su.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    def login_button():
        #**************** Description *****************************
        # Used in Log in Function to get log in info 
        # Matches login info from the login_info_database database
        # If info matched, moved to entry_system() otherwise popup
        #**********************************************************
        username_get = username_su.get()
        password_get = password_su.get()
        
        try: 
            if username_get == '' and password_get == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please Enter a Username and Password to Continue." 
                CTKlib.PopUpWindow.content(pop_up_root,text)

            if username_get == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please Enter a Username" 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            elif password_get == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please Enter a Password" 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            else:
                access_vec_1 = acc.login_check(username_get,password_get)
                access_vec = access_vec_1[0]
            
                try:
                    if access_vec == 'IT':
                        signup_root.destroy()
                        global new_user_root
                        new_user_root = CTKlib.Window()
                        new_user_root.title('Add User')
                        new_user_root.geometry('500x450')

                        username_au = customtkinter.CTkEntry(new_user_root,placeholder_text ='Username',corner_radius= 80)
                        username_au.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

                        password_au = customtkinter.CTkEntry(new_user_root,placeholder_text = 'Password',corner_radius = 80)
                        password_au.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

                        def on_option_selected(selected_option):
                            global access_type_new
                            access_type_new = selected_option
                        def close():
                            new_user_root.destroy()
                            login_root.deiconify()

                        options = ['Select',"full_access", "s_drill", "o_drill", "s_FT",'o_FT']

                        # Create the dropdown menu (CTkOptionMenu)
                        dropdown = customtkinter.CTkOptionMenu(new_user_root, values=options, command=on_option_selected,fg_color = 'green')
                        dropdown.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                        def add_user():
                            #**************** Description *****************************
                            # Used in Log in Function to get log in info 
                            # Matches login info from the login_info_database database
                            # If info matched, moved to entry_system() otherwise popup
                            #**********************************************************
                            username_get = username_au.get()
                            password_get = password_au.get()
                            
                            try: 
                                if username_get == '' and password_get == '':
                                    pop_up_root = CTKlib.PopUpWindow()
                                    text = "Please Enter a Username and Password to Continue." 
                                    CTKlib.PopUpWindow.content(pop_up_root,text)

                                if username_get == '':
                                    pop_up_root = CTKlib.PopUpWindow()
                                    text = "Please Enter a Username" 
                                    CTKlib.PopUpWindow.content(pop_up_root,text)
                                elif password_get == '':
                                    pop_up_root = CTKlib.PopUpWindow()
                                    text = "Please Enter a Password" 
                                    CTKlib.PopUpWindow.content(pop_up_root,text)
                                else:
                                    global access_type_new
                                    acc.sign_up(username_get,password_get,access_type_new)
                                    disp_text = customtkinter.CTkLabel(new_user_root, text='User added to the Database!', font=("Lufga Bold", 13,'bold'))
                                    disp_text.place(relx=0.35, rely=0.85)
                                    
                            except IndexError:
                                pop_up_root = CTKlib.PopUpWindow()
                                text = f"User Not Registered!\nPlease check the Login Database!." 
                                CTKlib.PopUpWindow.content(pop_up_root,text)
                            except TclError as e:
                                        print(f'{e}')
                            except Exception as e:
                                pop_up_root = CTKlib.PopUpWindow()
                                text = f"User or Database not found!\nCheck internet connection.\n{e}" 
                                CTKlib.PopUpWindow.content(pop_up_root,text)
                except IndexError:
                    pop_up_root = CTKlib.PopUpWindow()
                    text = f"User Not Registered!\nPlease check the Login Database!." 
                    CTKlib.PopUpWindow.content(pop_up_root,text)
                except TclError as e:
                            print(f'{e}')
                except Exception as e:
                    pop_up_root = CTKlib.PopUpWindow()
                    pop_up_root.geometry('600x400')
                    text = f"User or Database not found!\nCheck internet connection.\n{e}" 
                    CTKlib.PopUpWindow.content(pop_up_root,text)
                

                button = customtkinter.CTkButton(new_user_root, text = 'Add User',command = add_user,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80)
                button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

                button = customtkinter.CTkButton(new_user_root, text = 'Close',command = close,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80)
                button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        except TclError as e:
            print(f'{e}')
        except Exception as e:
            pop_up_root = CTKlib.PopUpWindow()
            pop_up_root.geometry('600x400')
            text = f"User or Database not found!\nCheck internet connection.\n{e}" 
            CTKlib.PopUpWindow.content(pop_up_root,text)
            
                
    button = customtkinter.CTkButton(signup_root, text = 'Log In',command = login_button,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80)
    button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

#==================Login System===================================

def login_system():
    #********************************************************************************************
    #Description: Generates the Log_in Window. Ask user inputs: Username, password.
    #             Input:  Void.
    #             Output: username and password to match with access database.   
    #********************************************************************************************
    global login_root
    login_root = CTKlib.Window()
    login_root.title('Log In')
    login_root.geometry('300x450')
    
    username = customtkinter.CTkEntry(login_root,placeholder_text ='Username',corner_radius= 80)
    username.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    password = customtkinter.CTkEntry(login_root,placeholder_text = 'Password',corner_radius = 80, show='•')
    password.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
   
    def sign_up_button():
            sign_up_menu()

    def login_button():
        #**************** Description *****************************
        # Used in Log in Function to get log in info 
        # Matches login info from the login_info_database database
        # If info matched, moved to entry_system() otherwise popup
        #**********************************************************
        username_get = username.get()
        password_get = password.get()
        
        try: 
            if username_get == '' and password_get == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please Enter a Username and Password to Continue." 
                CTKlib.PopUpWindow.content(pop_up_root,text)

            if username_get == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please Enter a Username" 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            elif password_get == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please Enter a Password" 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            else:
                global access_vec
                access_vec_1 = acc.login_check(username_get,password_get)
                access_vec = access_vec_1[0]

        except IndexError:
            pop_up_root = CTKlib.PopUpWindow()
            text = f"User Not Registered!\nPlease contact Johanson IT team for Support." 
            CTKlib.PopUpWindow.content(pop_up_root,text)
            
        try:
            #Takes to Access_Page.py
            login_root.destroy()
            Access_Page.access_level_logic(access_vec)
        except TclError as e:
                    print(f'{e}')
        except Exception as e:
            pop_up_root = CTKlib.PopUpWindow()
            pop_up_root.geometry('600x400')
            text = f"User or Database not found!\nCheck internet connection or contact Johanson IT team for Support.\n{e}" 
            CTKlib.PopUpWindow.content(pop_up_root,text)
            username.delete(0,'end')
            password.delete(0,'end')

    button = customtkinter.CTkButton(login_root, text = 'Log In',command = login_button,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80)
    button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    button = customtkinter.CTkButton(login_root, text = 'Sign up',command = sign_up_button,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80)
    button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        
