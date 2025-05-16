import CTKlib
import time
import access as acc 
import tkinter as tk
import customtkinter # <- import the CustomTkinter module
from tkinter import TclError
import re
import Sucess
#====================Edit Drill Entry System=========================
def drill_data_entry(part_info_vec,key,entry_root):
    #********************************************************************************************
    #Description: Generates the main data entry input Multi frame Window. 
    # Asks user inputs: OD/L,Thickness,ID1,warpage,(width,ID2,ID3) if required
    #             Input: part_info_vec --> part#, mo#, rev.
    #             Output: Void.   
    #********************************************************************************************
    entry_root.withdraw()
    start_time = time.time()
    drill_data_entry_root = CTKlib.MultiFrameWindow()
    drill_data_entry_root.title('Green Dimension Entry Form')
    frame_ID, drill_specs, part_info_vec = acc.verified_Drill_dimension_info(part_info_vec)
    try:
        if key == 'Edit Entry':
            orignal_data = acc.read_drill_database(part_info_vec)
            OD_L_ = orignal_data[3:13]
            Width_ = orignal_data[13:23]
            Thickness_w_ = orignal_data[23:33]
            Thickness_wo_ = orignal_data[33:43]
            ID1_ = orignal_data[43:53]
            ID2_ = orignal_data[53:63]
            ID3_ = orignal_data[63:73]
            Warpage_ = orignal_data[73:83]
        else:
            OD_L_ = ['','','','','','','','','','']
            Width_ = ['','','','','','','','','','']
            Thickness_w_ = ['','','','','','','','','','']
            Thickness_wo_ = ['','','','','','','','','','']
            ID1_ = ['','','','','','','','','','']
            ID2_ = ['','','','','','','','','','']
            ID3_ = ['','','','','','','','','','']
            Warpage_ = ['','','','','','','','','','']
        
    except IndexError:
        pop_up_root = CTKlib.PopUpWindow()
        text = f"No Entry Found!\n"
        CTKlib.PopUpWindow.content(pop_up_root,text)
    except TclError as e:
        print(f'{e}')
    except Exception as e:
        pop_up_root = CTKlib.PopUpWindow()
        text = f"{e}."
        CTKlib.PopUpWindow.content(pop_up_root,text)
   
    def gen_box_entry(frame, text, data):
        boxes = []  # Initialize an empty list to store references to entry boxes

        def focus_next(event):
            event.widget.tk_focusNext().focus()
            return 'break'  # Prevent the default behavior of the Enter key

        for i in range(10):
            row = i % 5  # Calculate the row number (0 to 4)
            col = i // 5  # Calculate the column number (0 or 1)

            x_offset = col * 0.5  # Adjust x offset based on column number
            y_offset = row * 0.1  # Adjust y offset based on row number

            box = customtkinter.CTkEntry(CTKlib.MultiFrameWindow.frames[frame], placeholder_text=f'{text} {i+1}', corner_radius=200, width=250, height=40)
            box.place(relx=0.1 + x_offset, rely=0.3 + y_offset)  # Adjust relx and rely based on offsets
            box.bind('<Return>', focus_next)  # Bind the Enter key event to focus on the next entry box
            if data and (i < len(data)) and (key == 'Edit Entry'):
                box.insert(0, data[i])  # Fill the entry box with data if available
            boxes.append(box)  # Store reference to each entry box in the list
        return boxes

    OD_L = []
    Width = []
    Thickness_w = []
    Thickness_wo = []
    ID1 = []
    ID2 = []
    ID3 = []
    Warpage = []
    

    
    def part_info_label(current_frame_ID,part_num,rev,mo_num):
        average_char_width = 8  # Adjust as needed
        padding = 160  # Adjust as needed
        text_length = max(len(part_info_vec[0]), len(part_info_vec[1]), len(part_info_vec[2]))
        box_width = text_length * average_char_width + padding

        # Create the rounded box with dynamic width
        rounded_box = customtkinter.CTkFrame(CTKlib.MultiFrameWindow.frames[current_frame_ID], width=box_width, height=90, corner_radius=10, fg_color='#086454')
        rounded_box.place(relx=0.01, rely=0.01)

        # Position the labels inside the rounded box
        label_pn = customtkinter.CTkLabel(rounded_box, text=f'Part Number \u25BA {part_num}', fg_color="#086454", font=("Lufga Bold", 16,'bold'))
        label_pn.place(relx=0.05, rely=0.05)
    
        label_rev = customtkinter.CTkLabel(rounded_box, text=f'Revision \u25BA {rev}', fg_color="#086454", font=("Lufga Bold", 16,'bold'))
        label_rev.place(relx=0.05, rely=0.3)
       
        label_mo = customtkinter.CTkLabel(rounded_box, text=f'MO Number \u25BA {mo_num}', fg_color="#086454", font=("Lufga Bold", 16,'bold'))
        label_mo.place(relx=0.05, rely=0.55)

    def header_info(current_frame_ID, data_min, data_max):  
        # Add labels or other content to the new frame as needed
        label1 = customtkinter.CTkLabel(CTKlib.MultiFrameWindow.frames[current_frame_ID], text=f'Green Part {current_frame_ID}', fg_color="#2e353e", font=("Lufga Bold", 46, "bold"))
        label1.pack(pady=30)

        label2 = customtkinter.CTkLabel(CTKlib.MultiFrameWindow.frames[current_frame_ID], text=f'Range \u25BA {data_min}" to {data_max}"', fg_color="#2e353e", font=("Lufga Bold", 20))
        label2.pack(pady=10)

    def review_info(current_frame_ID, mo_num):
        label1 = customtkinter.CTkLabel(CTKlib.MultiFrameWindow.frames[current_frame_ID], text=f'{current_frame_ID}', fg_color="#2e353e", font=("Lufga Bold", 50, "bold"))
        label1.pack(pady=30)
        # Calculate the center vertically

        bp1 = customtkinter.CTkLabel(CTKlib.MultiFrameWindow.frames[current_frame_ID], text=f'\u00BB Por favor, verifique que el número de MO sea correcto {mo_num}.', fg_color="#2e353e", font=("Lufga Bold", 30))
        bp1.place(relx=0.02, rely=0.3)  # Adjust rely to position it above center

        bp2 = customtkinter.CTkLabel(CTKlib.MultiFrameWindow.frames[current_frame_ID], text=f'\u00BB Por favor, llene todas las casillas de entrada para evitar errores.', fg_color="#2e353e", font=("Lufga Bold", 30))
        bp2.place(relx=0.02, rely=0.4)  # Center vertically

        bp3 = customtkinter.CTkLabel(CTKlib.MultiFrameWindow.frames[current_frame_ID], text=f'\u00BB Asegúrese de que todas las dimensiones sean consistentes con\nlos requisitos y especificaciones de la pieza que se está revisando.', fg_color="#2e353e", font=("Lufga Bold", 30))
        bp3.place(relx=0.02, rely=0.5)  # Adjust rely to position it below center

    Hover_color = '#086454'
    for i in range(len(frame_ID)):
        CTKlib.MultiFrameWindow.create_nav(drill_data_entry_root,frame_ID[i],Hover_color)
        if frame_ID[i] == 'OD':
            header_info(frame_ID[i],drill_specs[2],drill_specs[3])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            # Generate entry boxes
            text = 'OD'
            # OD_L = gen_box_entry(frame_ID[i],text)
            OD_L = gen_box_entry(frame_ID[i], text, OD_L_)
        elif frame_ID[i] == 'Length':
            header_info(frame_ID[i],drill_specs[2],drill_specs[3])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            # Generate entry boxes
            text = 'Length'
            # OD_L = gen_box_entry(frame_ID[i],text)
            OD_L = gen_box_entry(frame_ID[i], text, OD_L_)
        elif frame_ID[i] == 'Width':
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            header_info(frame_ID[i],drill_specs[4],drill_specs[5])
            # Generate entry boxes
            text = 'Width'
            # Width = gen_box_entry(frame_ID[i],text)
            Width = gen_box_entry(frame_ID[i], text, Width_)
        elif frame_ID[i] == 'Thickness\nWith Top Layer':
            header_info(frame_ID[i],drill_specs[6],drill_specs[7])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
             # Generate entry boxes
            text = 'Thickness With Top Layer'
            # Thickness_w = gen_box_entry(frame_ID[i],text)
            Thickness_w = gen_box_entry(frame_ID[i],text,Thickness_w_)
        elif frame_ID[i] == 'Thickness\nWithout Top Layer':
            header_info(frame_ID[i],drill_specs[8],drill_specs[9])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
             # Generate entry boxes
            text = 'Thickness Without Top Layer'
            # Thickness_wo = gen_box_entry(frame_ID[i],text,)
            Thickness_wo = gen_box_entry(frame_ID[i],text,Thickness_wo_)
        elif frame_ID[i] == 'ID A':
            header_info(frame_ID[i],drill_specs[10],drill_specs[11])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            # Generate entry boxes
            text = 'ID A'
            #ID1 = gen_box_entry(frame_ID[i],text)
            ID1 = gen_box_entry(frame_ID[i],text,ID1_)
        elif frame_ID[i] == 'ID B':
            header_info(frame_ID[i],drill_specs[12],drill_specs[13])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            text = 'ID B'
            # ID2 = gen_box_entry(frame_ID[i],text)
            ID2 = gen_box_entry(frame_ID[i],text,ID2_)
        elif frame_ID[i] == 'ID C':
            header_info(frame_ID[i],drill_specs[14],drill_specs[15])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            text = 'ID C'
            # ID3 = gen_box_entry(frame_ID[i],text)
            ID3 = gen_box_entry(frame_ID[i],text,ID3_)
        elif frame_ID[i] == 'Warpage':
            header_info(frame_ID[i],'0.000',drill_specs[16])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            text = 'Warpage'
            # Warpage = gen_box_entry(frame_ID[i],text)
            Warpage = gen_box_entry(frame_ID[i],text,Warpage_)
        elif frame_ID[i] == 'Review':
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            review_info(frame_ID[i],part_info_vec[1])
            def submit():
                try:
                    drill_dim_output = []
                    box_val_list = []
                    for box in OD_L:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in Width:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in Thickness_w:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in Thickness_wo:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in ID1:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in ID2:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in ID3:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in Warpage:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    #================Double Entry Check=================================
                    index = 0
                    index_2 = 1
                    for sublist in drill_dim_output:
                        for element in sublist:
                            if double_entry(element) == True:
                                ident = drill_box_identify(index)
                                pop_up_root = CTKlib.PopUpWindow()
                                text = f'Double entry at {ident} page. Box Number: {index_2}.\nYou entered: {element}.'
                                CTKlib.PopUpWindow.content(pop_up_root,text)
                            index_2+=1
                        index+=1
                        index_2 = 1
                    #====================================================================
                    #================No Entry Check=================================
                    index = 0
                    index_2 = 1
                    for sublist in drill_dim_output:
                        for element in sublist:
                            if element == '':
                                ident = drill_box_identify(index)
                                pop_up_root = CTKlib.PopUpWindow()
                                text = f'No Value detected at "{ident}" page.\nBox number: {index_2}.'
                                CTKlib.PopUpWindow.content(pop_up_root,text)
                            index_2+=1
                        index+=1
                        index_2 = 1
                    #================Non float entry Check==============================
                    index = 0
                    index_2 = 1
                    for sublist in drill_dim_output:
                        for element in sublist:
                            if is_number(element) == False:
                                ident = drill_box_identify(index)
                                pop_up_root = CTKlib.PopUpWindow()
                                text = f'Non number entry detected at "{ident}" page.\nBox number: {index_2}.\nYou entered {element}.'
                                CTKlib.PopUpWindow.content(pop_up_root,text)
                            index_2+=1
                        index+=1
                        index_2 = 1
                    #================Negative number entry Check==============================
                    index = 0
                    index_2 = 1
                    for sublist in drill_dim_output:
                        for element in sublist:
                            if float(element) < 0 :
                                ident = drill_box_identify(index)
                                pop_up_root = CTKlib.PopUpWindow()
                                text = f'Negative number entry detected at "{ident}" page.\nBox number: {index_2}.\nYou entered {element}.'
                                CTKlib.PopUpWindow.content(pop_up_root,text)
                            index_2+=1
                        index+=1
                        index_2 = 1
                    #====================================================================
                    #====================================================================
                    else: 
                        end_time = time.time()
                        if key == 'Edit Entry':
                            acc.edit_drill_database_table(part_info_vec,drill_dim_output,start_time,end_time)
                        else:
                            acc.write_to_drill_database(part_info_vec,drill_dim_output,start_time,end_time)
                            
                        Sucess.sucess_func()
                        drill_data_entry_root.destroy()
                except TclError as e:
                    print(f'{e}')
                except Exception as e:
                    pop_up_root = CTKlib.PopUpWindow()
                    text = f"{e}."
                    CTKlib.PopUpWindow.content(pop_up_root,text)

                
            button = customtkinter.CTkButton(CTKlib.MultiFrameWindow.frames[frame_ID[i]], text = 'Submit',command = submit,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width = 250, height = 60,font = ("Lufga Bold", 30))
            button.place(relx = 0.38,rely = 0.8)


#================Input Error Detection================================================
def double_entry(value):
    pattern = r'.*\..*\..*'  # Pattern to match at least two dots
    return bool(re.match(pattern, value))


def is_number(value):
    # Regular expression pattern to match numbers with optional decimal places
    pattern = r'^\d*\.?\d+$'
    # Match the input string against the pattern
    if re.match(pattern, value):
        return True
    else:
        return False

def drill_box_identify(i):
    print(i)
    if i == 0:
        return 'OD or Length'
    elif i == 1:
        return 'Width'
    elif i == 2:
        return 'Thickness with Cover Layers'
    elif i == 3:
        return 'Thickness without Cover Layers'
    elif i == 4:
        return 'ID 1'
    elif i == 5:
        return 'ID 2'
    elif i == 6:
        return 'ID 3'
    elif i == 7:
        return 'Warpage'
    
    