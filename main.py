from customtkinter import CTk, CTkLabel, CTkButton, CTkImage, CTkFrame, set_appearance_mode
from PIL import Image
import os


# window's

from window.home import HomeWidnow
set_appearance_mode('light')

class Video_to_text_gui:
    def __init__(self,window):
        self.window =window
        self.default_active_button_index = 0
        
        self.actions = {'home':HomeWidnow(self),}
        

    def button_handler(self, button, action):
        active_color = '#4070f4'
        default_color = '#ffffff'
        hover_color = '#a4a3aa'

        # Reset the previously active button
        if hasattr(self, 'active_button') and self.active_button:
            self.active_button.configure(fg_color=default_color, hover_color=hover_color)

        # Set the new active button
        button.configure(fg_color=active_color, hover_color=active_color)
        self.active_button = button

        # Call the action associated with the button
        action()

    def load_image(self, ico_path):
        if os.path.exists(ico_path):
            image = Image.open(ico_path)
            return CTkImage(light_image=image, dark_image=image, size=(24, 24))
        else:
            return None

    def gui(self):
        width, height = 1120, 720
        x, y = (self.window.winfo_screenwidth() // 2 - width // 2), (self.window.winfo_screenheight() // 2 - height // 2)

        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.side_bar = CTkLabel(master=self.window, width=210, height=2500, bg_color='white')
        self.side_bar.place(relx=0, rely=0)
        # element frame 
        
        self.element = CTkFrame(self.window,width=871,height=680,corner_radius=20)
        self.element.place(relx=0.2,rely=0.025)

        _ = CTkLabel(master=self.side_bar, text="SARK", font=('', 20, 'bold'), bg_color='white')
        _.place(relx=0.35, rely=0.0)

        # sidebar window
        button_frame = CTkFrame(master=self.side_bar, height=700, width=450, fg_color='white',bg_color='white')
        button_frame.place(relx=0.03, rely=0.05)
        icon_folder = os.path.join(os.getcwd(), 'assets', 'icon')

        self.side_bar_items = [
            {'name': 'Home               ', 'icon': os.path.join(icon_folder, "home.png"), 'action': lambda: self.actions['home'].show_home()},
            {'name': 'Subscription     ', 'icon': os.path.join(icon_folder, "wallet-filled-money-tool.png"), 'action': lambda: print('Subscription clicked')},
            {'name': 'Contact             ', 'icon': os.path.join(icon_folder, "email.png"), 'action': lambda: print('Contact clicked')},
            {'name': 'Feedback         ', 'icon': os.path.join(icon_folder, "feedback.png"), 'action': lambda: print('Feedback clicked')}
        ]

        # add buttons to sidebar
        buttons = []
        for i, item in enumerate(self.side_bar_items):
            name, ico_path, action = item['name'], item['icon'], item['action']

            icon = self.load_image(ico_path)
            print(f"\nImage Path: {ico_path}")
            print(icon)

            button = CTkButton(master=button_frame, text=name, image=icon, compound="left", width=180, height=42,
                               hover_color='#a4a3aa', text_color='black', fg_color='white')
            button.grid(row=i, column=0, pady=7)
            button.configure(command=lambda b=button, a=action: self.button_handler(b, a))
            buttons.append(button)

        self.active_button = buttons[self.default_active_button_index]
        self.button_handler(self.active_button, self.side_bar_items[self.default_active_button_index]['action'])

        self.window.mainloop()





app = Video_to_text_gui(CTk())
app.gui()