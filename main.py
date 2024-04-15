from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import json
import random
from random import choice

class Client:

    def __init__(self):
        with open("data/data.json") as f:
            self.data = json.load(f)

        self.quiz_main()

    def quiz_main(self):
        self.win = Tk()
        self.win.configure(bg='navy')
        self.win.title("Flag Quiz")
        self.win.iconbitmap("data/icon.ico")
        self.win.resizable(True, True)

        # Create a frame to hold all widgets
        self.frame = Frame(self.win, bg="navy")
        self.frame.grid(row=0, column=1, sticky="nsew")

        self.btnframe = Frame(self.win, bg="navy")
        self.btnframe.grid(row=1, column=1, sticky="ew")

        self.newframe = Frame(self.win, bg="blue")
        self.newframe.grid(row=0, column=2, sticky="e")

        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_columnconfigure(3, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_rowconfigure(4, weight=1)

        # Add weights to center the flag and options
        self.frame.grid_columnconfigure(0, weight=1)

        self.btnframe.grid_rowconfigure(0, weight=1)
        self.btnframe.grid_columnconfigure(0, weight=1)

        self.newframe.grid_rowconfigure(0, weight=1)
        self.newframe.grid_rowconfigure(5, weight=1)
        self.newframe.grid_columnconfigure(0, weight=1)

        self.indexes = list(range(len(self.data["country"])))

        self.topLabel = Label(self.frame, text="Flag Quiz", bg="navy", fg="ghost white", font=("MS Mincho", 24, "bold"))
        self.topLabel.grid(row=0, column=1, columnspan=1)

        self.answer = self.place_flag()

        self.option_buttons = []
        self.create_option_buttons()

        self.correct_answers = 0
        self.total_questions = 0
        self.helps_remaining = 3
        self.lives_remaining = 3

        self.score_label = Button(self.newframe, text=f"Score: {self.correct_answers}/{self.total_questions}", bg="navy", fg="green3", font=("MS Mincho", 16), bd=3)
        self.score_label.grid(row=1, column=0, padx=20, pady=15, sticky='nsew' )

        self.lives_label = Button(self.newframe, text=f"Lives Remaining: {self.lives_remaining}/3", bg="navy", fg="orange", font=("MS Mincho", 16), bd=3)
        self.lives_label.grid(row=3, column=0, padx=20, pady=10, sticky='nsew')

        self.help1 = Button(self.newframe, text=f"Help", bg="Green", font=("MS Mincho", 16), cursor='hand2', relief=RAISED, bd=4, padx=2, pady=2)
        self.help1.bind("<Button-1>", self.get_help)
        self.help1.grid(row=5, column=0, padx=20, pady=10, sticky='nsew')

        self.win.mainloop()

    def place_flag(self):
        country_data_ind = choice(self.indexes)
        self.indexes.remove(country_data_ind)

        flag_img_link = self.data["country"][country_data_ind]["link"]
        flag_img = Image.open(flag_img_link)

        # Calculate the aspect ratio to maintain proportions
        flag_width, flag_height = flag_img.size
        aspect_ratio = flag_width / flag_height

        # Define the maximum width and height for the flag display
        max_width = 712  # New width for the canvas
        max_height = 488  # New height for the canvas

        # Resize the flag image using Image.BILINEAR
        flag_img = flag_img.resize((max_width, max_height), Image.BILINEAR)

        self.canvas = Canvas(self.frame, bg="gray1", width=max_width, height=max_height, bd=2, relief="solid")
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_rowconfigure(5, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.canvas.grid(row=3, column=1, sticky='NSEW')

        if not self.indexes:
            messagebox.showinfo("Information", f"Quiz Ended with score: {self.correct_answers}/{self.total_questions}")
            self.win.destroy()
            Menu()
            return

        self.canvas.image = ImageTk.PhotoImage(flag_img)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)

        return self.data["country"][country_data_ind]["name"]

    def create_option_buttons(self):
        options = [self.answer]
        while len(options) < 4:
            option_data = random.choice(self.data["country"])
            if option_data['name'] not in options:
                options.append(option_data['name'])

        random.shuffle(options)  # Randomize the options

        max_name_length = max(len(option) for option in options)  # Find the length of the longest name
        button_width = max(20, max_name_length + 3)  # Set the button width to accommodate the longest name

        for i, option in enumerate(options):
            button = Button(self.btnframe, text=option, font=("MS Mincho", 16), command=lambda o=option: self.check_answer(o), width=button_width, height=2, cursor='hand2')  # Increase button size
            if i < 2:
                button.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')  # Reduce padx and pady for closer spacing
            else:
                button.grid(row=1, column=i-2, padx=10, pady=10, sticky='nsew')  # Reduce padx and pady for closer spacing
            self.option_buttons.append(button)

            # Bind hover events to change button color
            button.bind("<Enter>", lambda event, btn=button: btn.config(bg="Orange"))  # Change color on mouse enter
            button.bind("<Leave>", lambda event, btn=button: btn.config(bg="ghost white"))  # Restore color on mouse leave

    def check_answer(self, selected_option):
        self.total_questions += 1
        if selected_option == self.answer:
            self.correct_answers += 1
        else:
            self.lives_remaining -= 1
            if self.lives_remaining == 0:
                messagebox.showinfo("Information", f"Game Over! Your final score is: {self.correct_answers}")
                self.win.destroy()
                Menu()
                return
        self.update_scoreboard()
        self.canvas.destroy()
        for button in self.option_buttons:
            button.destroy()
        self.answer = self.place_flag()
        self.create_option_buttons()

    def get_help(self, event):
        if self.lives_remaining > 0:
            self.helps_remaining -= 1
            if self.helps_remaining >= 0:
                messagebox.showinfo("information", f"Answer: {self.answer} \nHelps Remaining: {self.helps_remaining}")
            else:
                messagebox.showinfo("information", "You have used up all your help chances!")

    def update_scoreboard(self):
        self.score_label.config(text=f"Score: {self.correct_answers}/{self.total_questions}")
        self.lives_label.config(text=f"Lives Remaining: {self.lives_remaining}/3")

class Menu:

    def __init__(self):
        self.gui_loop()

    def gui_loop(self):
        self.win = Tk()
        self.win.configure(bg='navy')
        self.win.title("Flag Quiz")
        self.win.iconbitmap("data/icon.ico")
        self.win.resizable(True, True)

        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_rowconfigure(0, weight=1)

        self.frame = Frame(self.win, bg="navy")
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.title = Label(self.frame, text="World Flag Quiz", bg="navy", fg="ghost white", font=("MS Mincho", 24, "bold"))
        self.title.grid(row=1, column=1)

        how_to_play = """
        How to Play:
        
        1) A random flag from countries around the world will be displayed.
        
        2) You will get 4 options from which you have to guess the correct option.
        
        3) You can only give 3 incorrect answers. After the 3rd incorrect answer, the game will end.
        
        4) You have a help button if you get stuck. However, you can only use it 3 times per game.
        
        5) You will have only 3 Helps in One Go
        """

        self.instructions_label = Label(self.frame, text=how_to_play, bg="navy", fg="ghost white", font=("MS Mincho", 14), justify=LEFT)
        self.instructions_label.grid(row=3, column=1, padx=20, pady=10, sticky='nsew')

        self.help = Label(self.frame, text=f"Play", bg="gray1", fg="ghost white", font=("MS Mincho", 22), cursor='hand2', relief=RAISED, bd=4, padx=20, pady=4)
        self.help.bind("<Button-1>", self.play_game)
        self.help.grid(row=4, column=1, sticky='N')

        self.win.mainloop()

    def play_game(self, event):
        self.win.destroy()
        client = Client()


if __name__ == "__main__":
    main = Menu()
