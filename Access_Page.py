import CTKlib
import access as acc
import Drill_Form
import Fired_Form
from tkinter import TclError
import tkinter as tk
import customtkinter # <- import the CustomTkinter module


def entry_info(Loc,Type):
    #********************************************************************************************
    #Description: Generates the new entry input Window. Asks user inputs: part#, mo#, and rev.
    #  Also contins input error checks. Then sends data to main_data_entry().
    #             Input:  Void.
    #             Output: Void.   
    #********************************************************************************************
    global part_info_vec
    global temp_access
    temp_access = False
    entry_root = CTKlib.Window()
    entry_root.title('Planar Array Information')

    def focus_next(event):
        event.widget.tk_focusNext().focus()
        return 'break'  # Prevent the default behavior of the Enter key

    part_number = customtkinter.CTkEntry(entry_root,placeholder_text ='Part Number',corner_radius= 80)
    part_number.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    part_number.bind('<Return>', focus_next)
    

    mo_number = customtkinter.CTkEntry(entry_root,placeholder_text = 'MO Number',corner_radius = 80)
    mo_number.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    mo_number.bind('<Return>', focus_next)

    rev = customtkinter.CTkEntry(entry_root,placeholder_text = 'Revision',corner_radius = 80)
    rev.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def pop_up():
        pop_up_root = CTKlib.PopUpWindow()
        text = "Entered information cannot be found in the database. Please re-enter the information"
        CTKlib.PopUpWindow.content(pop_up_root,text)
        part_number.delete(0, customtkinter.END)
        mo_number.delete(0, customtkinter.END)
        rev.delete(0, customtkinter.END)

    def submit_entry():
        try:
            partNumber = part_number.get()
            partNumber = partNumber.rstrip()
            moNumber = mo_number.get()
            moNumber = moNumber.rstrip()
            Rev = rev.get()
            #-----Pop-UP----------
            global Loc
            global pop_up_root
            if partNumber == '' and moNumber == '' and Rev == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please enter the Part Number, MO Number, and Revision to Continue."
                CTKlib.PopUpWindow.content(pop_up_root,text)

            elif partNumber != '' and moNumber == '' and Rev == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please enter the MO Number and Revision to Continue." 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            
            elif partNumber == '' and moNumber != '' and Rev == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please enter the Part Number and Revision to Continue."
                CTKlib.PopUpWindow.content(pop_up_root,text)

            elif partNumber == '' and moNumber == '' and Rev != '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please enter the Part Number and MO Number to Continue."
                CTKlib.PopUpWindow.content(pop_up_root,text)

            elif partNumber == '' and moNumber != '' and Rev != '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please enter the Part Number to Continue." 
                CTKlib.PopUpWindow.content(pop_up_root,text)

            elif partNumber != '' and moNumber == '' and Rev != '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please enter the MO Number to Continue." 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            
            elif partNumber != '' and moNumber != '' and Rev == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please enter the Revision to Continue." 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            
            else:
                part_info_vec = [acc.convert_upper(partNumber),moNumber,acc.convert_upper(Rev)]
                check = acc.entry_check(part_info_vec) # Checks in the database
                check_2 = acc.entry_check_drill(part_info_vec) # checks in the drill Database
                check_3 = acc.entry_check_FT(part_info_vec) # Checks in the Fire-test Database
                if Type == 'New Entry':
                    if check == True: # Check is PN in Database
                        if Loc == 'Drill' and Type == 'New Entry' and check_2 == False: # Check for duplicate entry
                            Drill_Form.drill_data_entry(part_info_vec,Type,entry_root)
                        elif Loc == 'Drill' and Type == 'New Entry' and check_2 == True: # Check for duplicate entry
                            pop_up_root = CTKlib.PopUpWindow()
                            text = "Entry already exists. No Duplicate entries allowed."
                            CTKlib.PopUpWindow.content(pop_up_root,text)
                        elif Loc == 'FT' and Type == 'New Entry':
                            if check_2 == True and check_3 == False: # checks if Drill entry exsists and FT doesn't
                                Fired_Form.FT_data_entry(part_info_vec,Type,entry_root)
                            elif check_2 == False and check_3 == False: # Condition: if No entry at Drill 
                                Loc = 'Drill'
                                global temp_access 
                                temp_access = True
                                Drill_Form.drill_data_entry(part_info_vec,Type,entry_root)
                            elif check_3 == True:
                                pop_up_root = CTKlib.PopUpWindow()
                                text = "Entry already exists. No Duplicate entries allowed."
                                CTKlib.PopUpWindow.content(pop_up_root,text)
            
                elif Loc == 'Drill' and Type == 'Edit Entry':
                    check = acc.entry_check_drill(part_info_vec)
                    if check == True:
                        Drill_Form.drill_data_entry(part_info_vec,Type)
                    else:
                        pop_up()
                elif Loc == 'FT' and Type == 'Edit Entry':
                    check = acc.entry_check_FT(part_info_vec)
                    if check == True:
                        Fired_Form.FT_data_entry(part_info_vec,Type,entry_root)
                    else:
                        pop_up()
                else:
                    pop_up()
                    
        
        except TclError as e:
                    print(f'{e}')
        except IndexError:
            pop_up()
        except Exception as e:
            pop_up_root = CTKlib.PopUpWindow()
            text = f"{e}."
            CTKlib.PopUpWindow.content(pop_up_root,text)
            # Add code for frame
            
       
    button = customtkinter.CTkButton(entry_root, text = 'Submit',command = submit_entry,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80)
    button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)



def full_access_system():
    #********************************************************************************************
    #Description: Provides a selection between new entry or view old entry.
    #             Input:  Void.
    #             Output: Void.    
    #********************************************************************************************
    global full_access_system_root
    full_access_system_root = CTKlib.Window()
    full_access_system_root.title('Main Menu')
    full_access_system_root.geometry('400x600')
    def run_query():
        full_access_system_root.withdraw()
        # query()
    def drill():
        full_access_system_root.withdraw()
        sup_drill()
    def ft():
        full_access_system_root.withdraw()
        sup_FT()

    button = customtkinter.CTkButton(full_access_system_root, text = 'Run Query',command = run_query,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width=220,height = 50,font=("Lufga Bold", 16,'bold'))
    button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    button = customtkinter.CTkButton(full_access_system_root, text = 'Drill Entry System',command = drill,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width=220,height = 50,font=("Lufga Bold", 16,'bold'))
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    button = customtkinter.CTkButton(full_access_system_root, text = 'Fire-Test Entry System',command = ft,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width=220,height = 50,font=("Lufga Bold", 16,'bold'))
    button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

#====================Supervisor Drill menu System==============================
def sup_drill():
    #********************************************************************************************
    #Description: Provides a selection between new entry or view old entry.
    #             Input:  Void.
    #             Output: Void.    
    #********************************************************************************************
    sup_drill_menu_root = CTKlib.Window()
    sup_drill_menu_root.title('Drill Main Menu')
    def drill_entry():
        global Loc
        global Type
        Loc = 'Drill'
        Type = 'New Entry'
        sup_drill_menu_root.withdraw()
        entry_info(Loc,Type)

    def edit_drill_entry():
        global Loc
        global Type
        Loc = 'Drill'
        Type = 'Edit Entry'
        sup_drill_menu_root.withdraw()
        entry_info(Loc,Type)

    button = customtkinter.CTkButton(sup_drill_menu_root, text = 'Drill Dimensions',command = drill_entry,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width=250,height = 50,font=("Lufga Bold", 16,'bold'))
    button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    button = customtkinter.CTkButton(sup_drill_menu_root, text = 'Edit Drill Dimensions',command = edit_drill_entry,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width=250,height = 50,font=("Lufga Bold", 16,'bold'))
    button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    
#==============================================================

#====================Entry System==============================
def sup_FT():
    #********************************************************************************************
    #Description: Provides a selection between new entry or view old entry.
    #             Input:  Void.
    #             Output: Void.    
    #********************************************************************************************
    sup_FT_menu_root = CTKlib.Window()
    sup_FT_menu_root.title('Fire Test Main Menu')
    def fired_entry():
        global Loc
        global Type
        Loc = 'FT'
        Type = 'New Entry'
        sup_FT_menu_root.withdraw()
        entry_info(Loc,Type)

    def edit_fired_entry():
        global Loc
        global Type
        Loc = 'FT'
        Type = 'Edit Entry'
        sup_FT_menu_root.withdraw()
        entry_info(Loc,Type)

    button = customtkinter.CTkButton(sup_FT_menu_root, text = 'Fired Dimensions',command = fired_entry,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width=250,height = 50,font=("Lufga Bold", 16,'bold'))
    button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    button = customtkinter.CTkButton(sup_FT_menu_root, text = 'Edit Fired Dimensions',command = edit_fired_entry,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width=250,height = 50,font=("Lufga Bold", 16,'bold'))
    button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def access_level_logic(access_vec):
    if access_vec == 'full_access':
        full_access_system()
    elif access_vec == 's_drill':
        sup_drill()
    elif access_vec == 's_FT':
        sup_FT()
    elif access_vec == 'o_drill':
        Loc = 'Drill'
        Type = 'New Entry'
        entry_info(Loc,Type)
    elif access_vec == 'o_FT':
        Loc = 'FT'
        Type = 'New Entry'
        entry_info(Loc,Type)
