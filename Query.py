import CTKlib
import access as acc
import Drill_Form
import Fired_Form
from tkinter import TclError
import Login
import tkinter as tk
import customtkinter # <- import the CustomTkinter module

#=================================================================
def query():
    #********************************************************************************************
    #Description: Opens a query window. Can access both Drill and FT Databases and Generate reports
    #             Input:  Void.
    #             Output: Void.    
    #********************************************************************************************
    global query_root
    query_root = CTKlib.Window()
    query_root.title('Query Menu')
    query_root.geometry('800x260')
    box_width = 785
    info_box = customtkinter.CTkFrame(query_root, width=box_width, height=250, corner_radius=10, fg_color='#787474')
    info_box.place(relx=0.01, rely=0.01)

    part_number = customtkinter.CTkEntry(info_box, placeholder_text='Part Number', width=250, height=35,
                                         corner_radius=80)
    part_number.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    mo_number = customtkinter.CTkEntry(info_box, placeholder_text='MO Number (optional)', width=250, height=35,
                                       corner_radius=80)
    mo_number.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    revision = customtkinter.CTkEntry(info_box, placeholder_text='Revision', width=250, height=35, corner_radius=80)
    revision.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def search():
        try:
            pn = part_number.get()
            mo = mo_number.get()
            rev = revision.get()
            query_vec = [pn, mo, rev]
            if pn == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please Enter a Part Number" 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            elif rev == '':
                pop_up_root = CTKlib.PopUpWindow()
                text = "Please Enter a Revision" 
                CTKlib.PopUpWindow.content(pop_up_root,text)
            else:
                switch_box_frame(query_vec)
        except IndexError:
            pop_up_root = CTKlib.PopUpWindow()
            text = f"Information Not Found!." 
            CTKlib.PopUpWindow.content(pop_up_root,text)

        except Exception as e:
                print(f'{e}')

    button = customtkinter.CTkButton(info_box, text='Search', command=search, fg_color='#3044bc',
                                            hover_color='#34eb7a', corner_radius=80)
    button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
#==============================================================================
def radio_generator(query_vec):
        frame_ID_drill, new_data, mod_part_info_vec = acc.verified_Drill_dimension_info(query_vec)
        frame_ID_ft, new_data, mod_part_info_vec = acc.verified_Fired_dimension_info(query_vec)
        return frame_ID_drill, frame_ID_ft
#==============================================================================
def switch_box_frame(query_vec):
    global query_root
    frame_ID_drill, frame_ID_ft = radio_generator(query_vec)
    frame_ID_drill.pop(len(frame_ID_drill) - 1)
    frame_ID_ft.pop(len(frame_ID_ft) - 1)
    query_root.geometry('800x850')
    query_root.update
    box_width = 785
    drill_info_box = customtkinter.CTkFrame(query_root, width=box_width, height=250, corner_radius=10,
                                            fg_color='#086454')
    drill_info_box.place(relx=0.01, rely=0.31)

    FT_info_box = customtkinter.CTkFrame(query_root, width=box_width, height=250, corner_radius=10,
                                            fg_color='#587ca4')
    FT_info_box.place(relx=0.01, rely=0.61)

    def gen_switches(frame_ID, parent_frame):
        switchers = []
        for i, frame in enumerate(frame_ID):
            row = i % 3  # Calculate the row number (0 to 2)
            col = i // 3  # Calculate the column number (0 to 2)

            x_offset = col * 0.5  # Adjust x offset based on column number
            y_offset = row * 0.2  # Adjust y offset based on row number

            switch_var = customtkinter.IntVar(value=0)  # Create a new IntVar for each switch
            switch = customtkinter.CTkSwitch(parent_frame, text=f"{frame}", onvalue=1, offvalue=0,
                                            variable=switch_var,font=("Lufga Bold", 16,'bold'))
            switch.place(relx=0.1 + x_offset, rely=0.2 + y_offset)  # Adjust relx and rely based on offsets

            switchers.append(switch_var)  # Append the IntVar to a list

        return switchers
    
    switchers_Drill = gen_switches(frame_ID_drill, drill_info_box)
    switchers_FT = gen_switches(frame_ID_ft, FT_info_box)

    def submit():
        drill_frame_switches = []
        ft_frame_switches = []
        for i in range(0,len(switchers_Drill)):
            drill_frame_switches.append(switchers_Drill[i].get())  # Print initial values of switches
        for i in range(0,len(switchers_FT)):
            ft_frame_switches.append(switchers_FT[i].get())  # Print initial values of switches
        acc.query(frame_ID_drill, frame_ID_ft,drill_frame_switches,ft_frame_switches)
    
    def back():
        global full_access_system_root
        query_root.destroy()
        full_access_system_root.deiconify()
    
    button = customtkinter.CTkButton(query_root, text='Submit', command=submit, fg_color='#3044bc',
                                            hover_color='#34eb7a', corner_radius=80)
    button.place(relx=0.8, rely=0.95, anchor=tk.CENTER)

    button = customtkinter.CTkButton(query_root, text='Back', command=back, fg_color='#3044bc',
                                            hover_color='#34eb7a', corner_radius=80)
    button.place(relx=0.2, rely=0.95, anchor=tk.CENTER)