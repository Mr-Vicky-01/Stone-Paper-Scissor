from tkinter import *
import threading
import cv2
import PIL.Image, PIL.ImageTk
from ai import Ai
from screen import Screen


class Interface():
    def __init__(self, screen: Screen):
        self.screen = screen
        self.window = Tk()
        self.ai = Ai()
        self.screen = Screen()
        self.window.config(bg="black")
        self.window.title("Stone Paper Scissor Game")
        self.window.config(pady=20, padx=20)
        self.rock_image = PhotoImage(file="rock.png").subsample(3, 3)
        self.paper_image = PhotoImage(file="paper.png").subsample(3, 3)
        self.scissor_image = PhotoImage(file="scissor.png").subsample(3, 3)

        self.title = Canvas(width=300, height=50, bg="black", highlightthickness=0)
        self.game_title = self.title.create_text(150, 25, text="Rock Paper Scissor", fill="lightgreen",
                                                  font=("ariel", 20, "bold"))
        self.title.grid(row=1, column=1,columnspan=3, pady=10)

        self.ai_canvas = Canvas(width=300, height=300, highlightthickness=0)
        self.ai_image = PhotoImage(file="Ai_robot2.png").subsample(2,2)
        self.image = self.ai_canvas.create_image(150, 150, image=self.ai_image)
        self.ai_text = self.ai_canvas.create_text(250, 25, text="", fill="red", font=("Arial", 23, "normal"))
        self.ai_canvas.grid(column=3, row=2)

        self.vs_circle = Canvas(width=100, height=100, highlightthickness=0, bg="black")
        circle = PhotoImage(file="red_circle.png")
        circle_resized = circle.subsample(20, 20)
        self.vs_circle.create_image(50, 50, image=circle_resized)
        self.circle_text = self.vs_circle.create_text(50, 50, text="V/S", fill="black", font=("Courier", 30, "bold"))
        self.vs_circle.grid(column=2, row=2, padx=15)

        self.button = Button(width=10,height=1,text="Start", highlightthickness=0, bg="lightblue",
                             font=("Courier", 20, "bold") ,command=self.timer)
        self.button.grid(row=3, column=1, pady=10, columnspan=3)

        self.comment = Label(text="Click a start to play", fg="white", bg="black", font=("Courier", 20, "bold"))
        self.comment.grid(row=4, column=1, columnspan=3, pady=5)

        self.video = Canvas(width=300, height=300, highlightthickness=0)
        self.video.grid(row=2, column=1)
        self.window.after(10, self.update_video_canvas)  # Schedule the update method

        # Create a thread to run the video processing
        video_thread = threading.Thread(target=self.screen.process_video)
        video_thread.start()

        self.window.mainloop()

    def update_video_canvas(self):
        frame = self.screen.get_current_frame()
        if frame is not None:
            img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.video.create_image(0, 0, anchor=NW, image=img)
            self.video.image = img  # Keep a reference to avoid garbage collection
        self.window.after(10, self.update_video_canvas)  # Schedule the next update

    def timer(self, count=3):
        self.ai_canvas.itemconfig(self.image, image=self.ai_image)
        self.ai_canvas.itemconfig(self.ai_text, text="")
        self.vs_circle.itemconfig(self.circle_text, text=str(count))
        self.update_comment(count)
        if count > 0:
            self.window.after(1000, self.timer, count - 1)
        else:
            self.vs_circle.itemconfig(self.circle_text, text="V/S")
            if self.screen.user_predicted == "":
                self.comment.config(text="Please Show the hand...")
                return
            who_win, ai_predicted = self.ai.who_wins_logic(self.screen.user_predicted)
            self.change_ai(ai_predicted)
            self.comment.config(text=who_win)
            self.blink_screen(who_win)

    def change_ai(self, ai_predicted):
        self.ai_canvas.coords(self.ai_text, 235, 25)
        if ai_predicted == "Rock":
            self.ai_canvas.itemconfig(self.image, image=self.rock_image)
            self.ai_canvas.itemconfig(self.ai_text ,text="Rock")
        elif ai_predicted == "Paper":
            self.ai_canvas.itemconfig(self.image, image=self.paper_image)
            self.ai_canvas.itemconfig(self.ai_text, text="Paper")
        elif ai_predicted == "Scissor":
            self.ai_canvas.itemconfig(self.image, image=self.scissor_image)
            self.ai_canvas.itemconfig(self.ai_text, text="Scissor")

    def update_comment(self, count):
        if count == 3:
            self.comment.config(text="Rock...")
        elif count == 2:
            self.comment.config(text="Paper...")
        elif count == 1:
            self.comment.config(text="Scissor...")

    def blink(self, count=6, color="white"):
        if count % 2 == 1:
            self.window.config(bg=color)
            self.vs_circle.config(bg=color)
            self.comment.config(bg=color)
            self.title.config(bg=color)
        else:
            self.window.config(bg="black")
            self.vs_circle.config(bg="black")
            self.comment.config(bg="black")
            self.title.config(bg="black")

        if count > 0:
            self.window.after(300, self.blink, count - 1, color)
        else:
            self.window.config(bg="black")
            self.vs_circle.config(bg="black")
            self.comment.config(bg="black")
            self.title.config(bg="black")

    def blink_screen(self, who_win):
        if who_win == "You Won":
            self.blink(count=6, color="green")
        elif who_win == "AI Win":
            self.blink(count=6, color="red")
        elif who_win == "Draw":
            self.blink(count=6, color="white")

