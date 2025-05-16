import CTKlib
import time
import access as acc 
import customtkinter # <- import the CustomTkinter module
from tkinter import TclError
import word_temp as wt
import Access_Page

def pdf_created(path):
    pdf_root = CTKlib.PopUpWindow()
    pdf_root.title('')
    text = f"PDF File sucessfully created!\nPath: {path}"
    CTKlib.PopUpWindow.content(pdf_root,text)
#==========================================================
def sucess_func():
    sucess_root = CTKlib.Window()
    sucess_root.geometry('600x700')
    sucess_root.title('Success')
    global access_vec
    global Loc
    global Type
    global part_info_vec
    global drill_specs
    global FT_specs
    global frame_ID

    bp1 = customtkinter.CTkLabel(sucess_root, text='SUCCESS!', fg_color="#242424", font=("Lufga Bold", 50))
    bp1.pack(pady = 30)  # Adjust rely to position it above center

    bp2 = customtkinter.CTkLabel(sucess_root, text='The information is uploaded to the server.', fg_color="#242424", font=("Lufga Bold", 30))
    bp2.pack(pady = 40)  # Center vertically

    def generate_report():
        progress_bar = customtkinter.CTkProgressBar(sucess_root, width=300, height=20,)
        progress_bar.pack(pady=20)
        if Loc == 'Drill':
            try:
                # Start the progress bar
                progress_bar.start()

                # Perform data processing (e.g., conversions and word drilling)
                part_info_vec[0] = acc.convert_upper(part_info_vec[0])
                part_info_vec[2] = acc.convert_upper(part_info_vec[2])
                path = wt.word_drill(part_info_vec, frame_ID)
                # Update progress and perform additional tasks
                progress_bar.update()
                sucess_root.update()
                time.sleep(1)
                wt.create_pdf(path,Loc)
                
                progress_bar.set(50)
                progress_bar.update()
                sucess_root.update()
                # Stop the progress bar
                progress_bar.stop()

                # Destroy the progress bar widget
                time.sleep(1)
                progress_bar.destroy()
                pdf_created(path)

            except TclError as e:
                    print(f'{e}')
            except Exception as e:
                pop_up_root = CTKlib.PopUpWindow()
                text = f"{e}."
                CTKlib.PopUpWindow.content(pop_up_root,text)
                
        elif Loc == 'FT':
            try:
                # Start the progress bar
                progress_bar.start()

                # Perform data processing (e.g., conversions and word drilling)
                part_info_vec[0] = acc.convert_upper(part_info_vec[0])
                part_info_vec[2] = acc.convert_upper(part_info_vec[2])
                path = wt.word_FT(part_info_vec, frame_ID,FT_specs)
                # Update progress and perform additional tasks
                progress_bar.update()
                sucess_root.update()
                time.sleep(1)
                wt.create_pdf(path,Loc)
                
                progress_bar.set(50)
                progress_bar.update()
                sucess_root.update()
                # Stop the progress bar
                progress_bar.stop()

                # Destroy the progress bar widget
                time.sleep(1)
                progress_bar.destroy()
                pdf_created(path)

            except TclError as e:
                    print(f'{e}')
            except Exception as e:
                pop_up_root = CTKlib.PopUpWindow()
                text = f"{e}."
                CTKlib.PopUpWindow.content(pop_up_root,text)

    def return_to_main():
        global temp_access
        global Loc
        if temp_access == True:
            Loc == 'FT'            
        Access_Page.access_level_logic()
        sucess_root.destroy()

    button_1 = customtkinter.CTkButton(sucess_root, text = 'Generate Report',command = generate_report,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width = 250, height = 60,font = ("Lufga Bold", 30))
    button_1.pack(pady = 70)

    button_2 = customtkinter.CTkButton(sucess_root, text = 'Return to Main Menu',command = return_to_main,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80,width = 250, height = 60,font = ("Lufga Bold", 30))
    button_2.pack(pady = 70)