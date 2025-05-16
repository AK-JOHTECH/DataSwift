import CTKlib
import re
import time
import access as acc 
import tkinter as tk
import customtkinter # <- import the CustomTkinter module
from tkinter import TclError

def cap_df(key):
    cap_df_root = CTKlib.MultiFrameWindow()
    # frame_ID, drill_specs, part_info_vec = acc.verified_Drill_dimension_info(part_info_vec)
    # part_info_vec = [acc.convert_upper(partNumber),moNumber,acc.convert_upper(Rev)]
    frame_ID, cap_specs, part_info_vec = ['Cap 1','Cap 2','Cap 3','Review'],[[1,2],[2,3],[3,4]],['12C16-A','223223-00','NCC-22']
    try:
        if key == 'Edit Entry':
            # orignal_data = acc.read_drill_database(part_info_vec)
            orignal_data = ['','','','','','','','','','']
            cap1_ = orignal_data[3:13]
            cap2_ = orignal_data[13:23]
            cap3_ = orignal_data[23:33]
            cap4_ = orignal_data[33:43]
            cap5_ = orignal_data[43:53]
        else:
            cap1_ = ['','','','','','','','','','']
            cap2_ = ['','','','','','','','','','']
            cap3_ = ['','','','','','','','','','']
            cap4_ = ['','','','','','','','','','']
            cap5_ = ['','','','','','','','','','']
            
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
        boxes = []  # Store references to entry boxes

        def focus_next(event):
            event.widget.tk_focusNext().focus()
            return 'break'

        for i in range(20):
            row = i % 5
            col = i // 5

            # Define custom horizontal positions for 4 columns
            if col == 0:
                relx = 0.1  # Cap 1–5
            elif col == 1:
                relx = 0.25  # DF 1–5 (close to column 0)
            elif col == 2:
                relx = 0.55  # Cap 6–10 (large gap from col 1)
            elif col == 3:
                relx = 0.7  # DF 6–10 (close to column 2)

            rely = 0.3 + row * 0.1

            box = customtkinter.CTkEntry(
                CTKlib.MultiFrameWindow.frames[frame],
                placeholder_text=f'{text} {i+1}',
                corner_radius=200,
                width=150,
                height=40
            )
            box.place(relx=relx, rely=rely)
            box.bind('<Return>', focus_next)

            if data and (i < len(data)) and (key == 'Edit Entry'):
                box.insert(0, data[i])
            boxes.append(box)

        return boxes

    cap1 = []
    cap2 = []
    cap3 = []
    cap4 = []
    cap5 = []
    

    
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
        label1 = customtkinter.CTkLabel(CTKlib.MultiFrameWindow.frames[current_frame_ID], text=f'{current_frame_ID}', fg_color="#2e353e", font=("Lufga Bold", 46, "bold"))
        label1.pack(pady=30)

        label2 = customtkinter.CTkLabel(CTKlib.MultiFrameWindow.frames[current_frame_ID], text=f'Range \u25BA {data_min} nF to {data_max} nF', fg_color="#2e353e", font=("Lufga Bold", 20))
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
        CTKlib.MultiFrameWindow.create_nav(cap_df_root,frame_ID[i],Hover_color)
        if frame_ID[i] == 'Cap 1':
            header_info(frame_ID[i],cap_specs[0][0],cap_specs[0][1])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            # Generate entry boxes
            text = 'Capacitance 1'
            # OD_L = gen_box_entry(frame_ID[i],text)
            cap1 = gen_box_entry(frame_ID[i], text, cap1_)
        elif frame_ID[i] == 'Cap 2':
            header_info(frame_ID[i],cap_specs[1][0],cap_specs[1][1])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            # Generate entry boxes
            text = 'Capacitance 2'
            # OD_L = gen_box_entry(frame_ID[i],text)
            cap2 = gen_box_entry(frame_ID[i], text, cap2_)
        elif frame_ID[i] == 'Cap 3':
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            header_info(frame_ID[i],cap_specs[2][0],cap_specs[2][1])
            # Generate entry boxes
            text = 'Capacitance 3'
            # Width = gen_box_entry(frame_ID[i],text)
            cap3 = gen_box_entry(frame_ID[i], text, cap3_)
        elif frame_ID[i] == 'Cap 4':
            header_info(frame_ID[i],cap_specs[3][0],cap_specs[3][1])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
             # Generate entry boxes
            text = 'Capacitance 4'
            # Thickness_w = gen_box_entry(frame_ID[i],text)
            cap4 = gen_box_entry(frame_ID[i],text,cap4_)
        elif frame_ID[i] == 'Cap 5':
            header_info(frame_ID[i],cap_specs[4][0],cap_specs[4][1])
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
             # Generate entry boxes
            text = 'Capacitance 5'
            # Thickness_wo = gen_box_entry(frame_ID[i],text,)
            cap5 = gen_box_entry(frame_ID[i],text,cap5_)
        elif frame_ID[i] == 'Review':
            part_info_label(frame_ID[i],part_info_vec[0],part_info_vec[2],part_info_vec[1])
            review_info(frame_ID[i],part_info_vec[1])
            def submit():
                try:
                    drill_dim_output = []
                    box_val_list = []
                    for box in cap1:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in cap2:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in cap3:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in cap4:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    for box in cap5:  # Iterate over each entry box in the list
                        bx = box.get()  # Retrieve value from each entry box separately
                        box_val_list.append(bx)
                    drill_dim_output.append(box_val_list)
                    box_val_list = []
                    #================Double Entry Check=================================
                    index = 0
                    index_2 = 1
                    for sublist in drill_dim_output:
                        for element in sublist:
                            if double_entry(element) == True:
                                ident = cap_box_identify(index)
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
                                ident = cap_box_identify(index)
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
                                ident = cap_box_identify(index)
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
                                ident = cap_box_identify(index)
                                pop_up_root = CTKlib.PopUpWindow()
                                text = f'Negative number entry detected at "{ident}" page.\nBox number: {index_2}.\nYou entered {element}.'
                                CTKlib.PopUpWindow.content(pop_up_root,text)
                            index_2+=1
                        index+=1
                        index_2 = 1
                    #====================================================================
                    #====================================================================
                    else: 
                        # end_time = time.time()
                        # acc.edit_drill_database_table(part_info_vec,drill_dim_output,start_time,end_time)
                        # Sucess.sucess_func()
                        cap_df_root.destroy()
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

def cap_box_identify(i):
    print(i)
    if i == 0:
        return 'Cap 1'
    elif i == 1:
        return 'Cap 2'
    elif i == 2:
        return 'Cap 3'
    elif i == 3:
        return 'Cap 4'
    elif i == 4:
        return 'Cap 5'
    

if __name__ == "__main__":
    global root
    root = customtkinter.CTk()
    key = ''
    cap_df(key)
    root.mainloop()
