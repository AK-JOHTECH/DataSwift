import tkinter as tk
import customtkinter # <- import the CustomTkinter module
import os
from functools import partial
# Set theam and color options
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

#====================================================================

#===============Window Class Object==================================
class Window(customtkinter.CTkToplevel): 
    #********************************************************************************************
    #Description: This class is used to create the main windows and connecting windows. 
        # It connects the main root to all the sub windows. It also sets a default size 
        # for a window, but size can be changed using sub roots. 
    # Functions: None
    #********************************************************************************************
    def __init__(self):
        super().__init__()
        self.geometry('400x600')
        self.protocol('WM_DELETE_WINDOW',self.end_program)
    
    def end_program(self):
        self.quit()  # Terminate the main event loop
        self.destroy()  # Destroy the root window
        os._exit(0)  # Ensure the program exits completely
#====================================================================

    
#===============Pop Up Class Object==================================
class PopUpWindow(customtkinter.CTkToplevel): 
    #********************************************************************************************
    #Description: This class is used to create all the pop up windows.
    # Functions: content 
  
    #********************************************************************************************
    def __init__(self):
        super().__init__()
        self.title('Error')
        self.geometry('600x150')
 

    def content(self,Text):
        #********************************************************************************************
        #Description: (public) This function displays the error message. All the attributes like font size,
        #   color, and close button can be  set here.
        #             Input: Error message. 
        #             Output: Void.  
        #********************************************************************************************
        error_message = customtkinter.CTkLabel(self, text = Text) 
        error_message.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        def close_popup():
        #********************************************************************************************
        #Description: This function shuts down the pop up window root. 
        #             Input: Void. 
        #             Output: Void.  
        #********************************************************************************************
            self.destroy()

        button = customtkinter.CTkButton(self, text = 'OK',command = close_popup,fg_color = 'green',hover_color='#34eb7a',corner_radius = 80)
        button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.grab_set()  # Prevent interaction with the main window
        self.wait_window()  # Wait until the pop-up window is closed
        self.grab_release()
        self.protocol('WM_DELETE_WINDOW',close_popup)
#====================================================================
#===============Multi-Tab Window Class Object========================
class MultiFrameWindow(customtkinter.CTkToplevel):
    #********************************************************************************************
    #Description: This class is used to Multi frame input window. 
        # Edit frame selector buttons, and frame sizes. 
    # Functions:
    # frame_selector_bt, create_frame, toggle_frame_by_id, create_nav
    #********************************************************************************************
    global frame_id
    frames = {}
    frame_order = []
    current = None
    bg = ""
    current_frame_index = 0
    frame_buttons = {}  # Store references to frame selector buttons
    def __init__(self):
        super().__init__()
        self.bg = self.cget("fg_color")
        self.num_of_frames = 1
        self.geometry("1200x850")
        self.protocol('WM_DELETE_WINDOW',self.end_program)

        main_container = customtkinter.CTkFrame(self, corner_radius=8, fg_color=self.bg)
        main_container.pack(fill=customtkinter.BOTH, expand=True, padx=8, pady=8)

        self.left_side_panel = customtkinter.CTkFrame(main_container, width=280, corner_radius=8, fg_color=self.bg)
        self.left_side_panel.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, padx=18, pady=10)

        self.right_side_panel = customtkinter.CTkFrame(main_container, corner_radius=30, fg_color="#2e353e")
        self.right_side_panel.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True, padx=0, pady=0)
        self.right_side_panel.configure(border_width=1)
        self.right_side_panel.configure(border_color="#2e353e")
    
    def end_program(self):
        self.quit()  # Terminate the main event loop
        self.destroy()  # Destroy the root window
        os._exit(0)  # Ensure the program exits completely
        
    def frame_selector_bt(self, frame_id,Hover_color):
        #********************************************************************************************
        #Description: (public) Used to generate selector buttons for the frame.
        #             Input: root, button location, button/frame name 
        #             Output: Void.  
        #********************************************************************************************
        bt_frame = customtkinter.CTkButton(self.left_side_panel)
        bt_frame.configure(height=40,fg_color = '#232323', hover_color=Hover_color,corner_radius = 20) # Change frame button dimensions.

        bt_frame.configure(text=frame_id,font=("Lufga Bold", 14, "bold"))
        bt_frame.configure(command=partial(self.toggle_frame_by_id, frame_id))
        bt_frame.grid(pady=10, row=self.num_of_frames, column=0)
        self.num_of_frames += 1

        self.frame_buttons[frame_id] = (bt_frame, Hover_color)  # Store button reference and hover color

    def create_frame(self, frame_id,Hover_color):
        #********************************************************************************************
        #Description: (public) Used to customize the frame color and borders.
        #             Input: root, button/frame name 
        #             Output: Void.  
        #********************************************************************************************
        self.frames[frame_id] = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.frames[frame_id].configure(corner_radius=10)
        self.frames[frame_id].configure(fg_color="#2e353e")
        self.frames[frame_id].configure(border_width=20)
        self.frames[frame_id].configure(border_color="#2e353e")
        self.frames[frame_id].pack_forget()

        next_button = customtkinter.CTkButton(self.frames[frame_id], text='Next \u2B9E', command=self.go_to_next_frame, fg_color='#2e353e', hover_color=Hover_color, corner_radius=20, font=("Lufga Bold", 16, "bold"))
        next_button.place(relx=0.85, rely=0.9, anchor=tk.E)

        back_button = customtkinter.CTkButton(self.frames[frame_id], text='\u2B9C Back', command=self.go_to_previous_frame, fg_color='#2e353e', hover_color=Hover_color, corner_radius=20, font=("Lufga Bold", 16, "bold"))
        back_button.place(relx=0.1, rely=0.9, anchor=tk.W)

        # Store button references in the frame dictionary
        self.frames[frame_id].next_button = next_button
        self.frames[frame_id].back_button = back_button
      

    def toggle_frame_by_id(self, frame_id):
        #********************************************************************************************
        #Description: (public) Allows toggle between different frames.
        #             Input: root, button/frame name 
        #             Output: Void.  
        #********************************************************************************************
        if self.frames[frame_id] is not None:
            new_frame = self.frames[frame_id]
            if self.current is not None:
                if self.current is new_frame:
                    self.current.pack_forget()
                    self.current = None
                else:
                    self.current.pack_forget()
                    self.current = new_frame
                    self.current.pack(in_=self.right_side_panel, side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True, padx=0, pady=0)
            else:
                self.current = new_frame
                self.current.pack(in_=self.right_side_panel, side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True, padx=0, pady=0)

            self.current_frame_index = self.frame_order.index(frame_id)
            self.update_frame_button_colors(frame_id)
            self.update_navigation_buttons()
        else:
            pop_up_root = PopUpWindow()
            pop_up_root.geometry('600x400')
            text = f"Frame with ID {frame_id} does not exist or is None."
            PopUpWindow.content(pop_up_root,text)

    
    def create_nav(self, frame_id,Hover_color):
        #********************************************************************************************
        #Description: (public) innitiator funtion for frame_selector_bt and create_frame.
        #             Input: root, button/frame name 
        #             Output: Void.  
        #********************************************************************************************
        self.frame_selector_bt(frame_id,Hover_color)
        self.create_frame(frame_id,Hover_color)
        self.frame_order.append(frame_id)

    def go_to_previous_frame(self):
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            frame_id = self.frame_order[self.current_frame_index]
            self.toggle_frame_by_id(frame_id)
        
    def go_to_next_frame(self):
        if self.current_frame_index < len(self.frame_order) - 1:
            self.current_frame_index += 1
            frame_id = self.frame_order[self.current_frame_index]
            self.toggle_frame_by_id(frame_id)

    def update_navigation_buttons(self):
        if self.current_frame_index == 0:
            self.frames[self.frame_order[0]].back_button.place_forget()
        else:
            self.frames[self.frame_order[0]].back_button.place(relx=0.1, rely=0.9, anchor=tk.W)

        if self.current_frame_index == len(self.frame_order) - 1:
            self.frames[self.frame_order[-1]].next_button.place_forget()
        else:
            self.frames[self.frame_order[-1]].next_button.place(relx=0.85, rely=0.9, anchor=tk.E)

    def update_frame_button_colors(self, selected_frame_id):
        for frame_id, (button, hover_color) in self.frame_buttons.items():
            if frame_id == selected_frame_id:
                button.configure(fg_color=hover_color)
            else:
                button.configure(fg_color='#232323')
        