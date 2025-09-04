import tkinter as tk
import random
from tkinter import messagebox

# Game of Thrones trivia questions and answers
# This list holds all the questions, options, and correct answers for the quiz.
QUESTIONS = [
    {
        "question": "What is the name of the white direwolf that Jon Snow finds?",
        "options": ["Nymeria", "Ghost", "Shaggydog", "Summer"],
        "answer": "Ghost"
    },
    {
        "question": "Which family's sigil is a golden lion on a crimson field?",
        "options": ["House Stark", "House Baratheon", "House Lannister", "House Targaryen"],
        "answer": "House Lannister"
    },
    {
        "question": "What title is given to the leader of the Night's Watch?",
        "options": ["King Beyond the Wall", "Lord Commander", "Master of Coin", "Hand of the King"],
        "answer": "Lord Commander"
    },
    {
        "question": "Which character is known as the 'Kingslayer'?",
        "options": ["Tyrion Lannister", "Jaime Lannister", "Jorah Mormont", "The Hound"],
        "answer": "Jaime Lannister"
    },
    {
        "question": "In which city is the Iron Throne located?",
        "options": ["Winterfell", "Casterly Rock", "King's Landing", "Dragonstone"],
        "answer": "King's Landing"
    },
    {
        "question": "What is the family motto of House Greyjoy?",
        "options": ["Hear Me Roar!", "Ours is the Fury", "We Do Not Sow", "Unbowed, Unbent, Unbroken"],
        "answer": "We Do Not Sow"
    },
    {
        "question": "Which sword is known as the 'Widow's Wail'?",
        "options": ["Longclaw", "Oathkeeper", "Ice", "Widow's Wail"],
        "answer": "Widow's Wail"
    },
    {
        "question": "What is the name of the master of Whisperers?",
        "options": ["Petyr Baelish", "Varys", "Grand Maester Pycelle", "Davos Seaworth"],
        "answer": "Varys"
    }
]

class TriviaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game of Thrones Trivia")
        self.root.geometry("600x450")
        self.root.configure(bg="#000000")

        self.score = 0
        self.current_question_index = 0
        self.lifeline_used = False
        self.timer_id = None

        self.questions = QUESTIONS.copy()
        random.shuffle(self.questions)

        self.setup_ui()
        self.show_next_question()

    def setup_ui(self):
        # Main content frame to center and add padding
        self.content_frame = tk.Frame(self.root, bg="#000000")
        self.content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title Label
        self.title_label = tk.Label(self.content_frame, text="Game of Thrones Trivia", font=("Trajan Pro", 24, "bold"), fg="#FFD700", bg="#000000")
        self.title_label.pack(pady=10)

        # Score Label
        self.score_label = tk.Label(self.content_frame, text="Score: 0", font=("Arial", 14), fg="white", bg="#000000")
        self.score_label.pack(pady=5)
        
        # Timer label
        self.timer_label = tk.Label(self.content_frame, text="Time: 20", font=("Arial", 14), fg="#DC143C", bg="#000000")
        self.timer_label.pack(pady=5)

        # Question Label
        self.question_label = tk.Label(self.content_frame, text="", font=("Arial", 16), fg="white", bg="#000000", wraplength=500)
        self.question_label.pack(pady=20)

        # Options frame to hold the answer buttons
        self.options_frame = tk.Frame(self.content_frame, bg="#000000")
        self.options_frame.pack(pady=10)
        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.options_frame, text="", font=("Arial", 12), width=30, bg="#474747", fg="white", activebackground="#606060", activeforeground="white", bd=0, relief="flat", command=lambda i=i: self.check_answer(self.option_buttons[i]['text']))
            button.pack(pady=5)
            self.option_buttons.append(button)

        # Lifeline button
        self.lifeline_button = tk.Button(self.content_frame, text="50/50 Lifeline", font=("Arial", 12), bg="#474747", fg="white", activebackground="#606060", activeforeground="white", bd=0, relief="flat", command=self.use_lifeline)
        self.lifeline_button.pack(pady=10)

    def show_next_question(self):
        # Cancel any previous timer to prevent multiple timers running
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        # Check if there are more questions
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.config(text=question_data["question"])
            
            # Shuffle the options for variety
            options_shuffled = question_data["options"].copy()
            random.shuffle(options_shuffled)

            # Update button text and state
            for i, option_text in enumerate(options_shuffled):
                self.option_buttons[i].config(text=option_text, state=tk.NORMAL, bg="#474747")
            
            # Start a new timer
            self.time_left = 20
            self.countdown()
        else:
            self.end_game()

    def countdown(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.countdown)
        else:
            self.check_answer(None)

    def use_lifeline(self):
        # Lifeline can only be used once
        if not self.lifeline_used:
            self.lifeline_used = True
            self.lifeline_button.config(state=tk.DISABLED)
            
            question_data = self.questions[self.current_question_index]
            correct_answer = question_data["answer"]
            
            # Find two incorrect options to disable
            incorrect_options = [opt for opt in question_data["options"] if opt != correct_answer]
            options_to_disable = random.sample(incorrect_options, 2)
            
            # Disable the buttons
            for button in self.option_buttons:
                if button['text'] in options_to_disable:
                    button.config(state=tk.DISABLED, bg="#333333")

    def check_answer(self, selected_answer):
        # Stop the timer when an answer is submitted
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        question_data = self.questions[self.current_question_index]
        correct_answer = question_data["answer"]

        # Check for a correct answer or timeout
        if selected_answer == correct_answer:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            messagebox.showinfo("Correct!", "That's right! You're a true fan.")
        elif selected_answer is None:
            messagebox.showerror("Time's Up!", f"You ran out of time! The correct answer was {correct_answer}.")
        else:
            messagebox.showerror("Incorrect!", f"Wrong! The correct answer was {correct_answer}.")
        
        # Move to the next question
        self.current_question_index += 1
        self.show_next_question()

    def end_game(self):
        messagebox.showinfo("Game Over!", f"You finished the quiz!\nYour final score is: {self.score}/{len(QUESTIONS)}")
        self.root.destroy()

# The entry point for the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaApp(root)
    root.mainloop()
