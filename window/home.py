import tkinter as tk
from tkinter import filedialog
from customtkinter import CTk, CTkImage, CTkLabel, CTkButton, CTkFrame, set_appearance_mode
from PIL import Image
import os 
from threading import Thread
from tkinter import messagebox
import shutil
# scripts
from libs.video_to_audio import convert_audio

set_appearance_mode('light')

class HomeWidnow:
    
    def __init__(self, main_window):
        self.window = main_window
        self.file_path = None
        
    def start_action(self):
        
        if self.file_path!=None:
            
            img_pth = os.path.join(os.getcwd(),'assets','images','9251270.png')
            img = Image.open(img_pth)
            
            indicator_img = CTkImage(light_image=img,dark_image=img,size=(250,250))
            self.indicator_lable.configure(image=indicator_img)
            
            self.process_info.configure(text='Processing')
            th = Thread(target=convert_audio,args=(self.file_path,self.indicator_lable,self.process_info,self.writing_lable))
            th.start()
            self.writing_lable.configure(text='Genareting text....')
        else:
            messagebox.showerror(title='FileNotFound',message='please select a video file first!')
                
        
        
        
        
            
    def open_file_dialog(self):
        # Open file dialog to select mp4 or video files
        self.file_path = filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4"), ("Video Files", "*.avi;*.mp4;*.mkv;*.mov")])
        
        if self.file_path:
            # If a file is selected, update the label to show the file path
            self.file_select_info.configure(text="Selected") # Display only the file name
            self.process_info.configure(text="Good to go 👍")
            self.start_btn.configure(fg_color='#4070f4')


    def download_file(self):
        transcription_file = "transcription.txt"  # Path to the file with the transcription

        if os.path.exists(transcription_file):  # Check if the file exists
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                initialfile="sark_transcoding_data"
            )
            if save_path:
                try:
                    # Move the transcription file to the selected location
                    shutil.move(transcription_file, save_path)
                    messagebox.showinfo(title="Success", message="File moved successfully!")
                except Exception as e:
                    messagebox.showerror(title="Error", message=f"An error occurred: {e}")
            else:
                messagebox.showwarning(title="Cancelled", message="Save operation was cancelled.")
        else:
            messagebox.showerror(title="File Not Found", message="No transcription file found to save. Please process a file first.")


    def show_home(self):
        for widget in self.window.element.winfo_children():
            widget.destroy()
            print(widget)
              
        
        # upload frame element

        
        self.upload_farame = CTkFrame(master=self.window.element, fg_color='white', width=350, height=150, corner_radius=20)
        self.upload_farame.place(relx=0.035, rely=0.025)
        ##########33
        add_path = os.path.join(os.getcwd(),'assets','icon','add-file.png')
        image = Image.open(add_path)
        
        img1 = CTkImage(light_image=image,dark_image=image,size=(32,32))
        
        btn1 = CTkButton(master=self.upload_farame,image=img1,text='',fg_color='white',hover_color='#a4a3aa',width=60,
                         command=self.open_file_dialog)
        btn1.place(relx=0.55,rely=0.12)
        
        ####
        dwn_path = os.path.join(os.getcwd(),'assets','icon','download.png')
        image = Image.open(dwn_path)
        
        img = CTkImage(light_image=image,dark_image=image,size=(24,24))
        
        dwn_btn = CTkButton(master=self.upload_farame,image=img,text='',fg_color='white',hover_color='#a4a3aa',width=60,command=self.download_file)
        dwn_btn.place(relx=0.8,rely=0.55)
        
        _ = CTkLabel(master=self.upload_farame, text='Select your video', font=('', 15, 'bold'))
        _.place(relx=0.015, rely=0.05)
        
        info_fm = CTkFrame(master=self.upload_farame, height=55, corner_radius=25, width=250)
        info_fm.place(relx=0.025, rely=0.5)   
        
        self.file_select_info = CTkLabel(master=info_fm, text='Not selected')
        self.file_select_info.place(relx=0.51, rely=0.2)     
        
        select_btn = CTkButton(master=info_fm, text='File', width=90, corner_radius=25, height=45, command=self.open_file_dialog)
        select_btn.place(relx=0.06, rely=0.09)
        
        
        
        loading_frame = CTkFrame(master=self.window.element,fg_color='white',width=350,height=450,corner_radius=25)
        loading_frame.place(relx=0.035,rely=0.3)
        
        self.process_info = CTkLabel(master=loading_frame,text='File not selected yet',font=('',15))
        self.process_info.place(relx=0.09,rely=0.11)
        
        self.start_btn = CTkButton(master=loading_frame,text='Start',height=35,width=80,fg_color='#F16B6C',command=self.start_action)
        self.start_btn.place(relx=0.65,rely=0.11)
        
        
        self.indicator_lable = CTkLabel(master=loading_frame,text='')
        self.indicator_lable.place(relx=0.15,rely=0.3)
        # writting pad 
        
        self.writing_fram = CTkFrame(master=self.window.element,fg_color='white',width=436,height=650,corner_radius=25)
        self.writing_fram.place(relx=0.48,rely=0.025)
        
        self.writing_lable = CTkLabel(master=self.writing_fram,text='',justify="left",anchor="w",wraplength=400 )
        self.writing_lable.place(relx=0.02,rely=0.015)