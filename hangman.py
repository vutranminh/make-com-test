import tkinter as tk
import random

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman")
        self.master.geometry("400x500")

        self.words = ["python", "programming", "computer", "algorithm", "database"]
        self.max_tries = 6
        self.current_word = ""
        self.guessed_letters = set()
        self.tries_left = self.max_tries

        self.hangman_stages = [
            """
               ____
              |    |
              |
              |
              |
              |
            __|__
            """,
            """
               ____
              |    |
              |    O
              |
              |
              |
            __|__
            """,
            """
               ____
              |    |
              |    O
              |    |
              |
              |
            __|__
            """,
            """
               ____
              |    |
              |    O
              |   /|
              |
              |
            __|__
            """,
            """
               ____
              |    |
              |    O
              |   /|\\
              |
              |
            __|__
            """,
            """
               ____
              |    |
              |    O
              |   /|\\
              |   /
              |
            __|__
            """,
            """
               ____
              |    |
              |    O
              |   /|\\
              |   / \\
              |
            __|__
            """
        ]

        self.hangman_label = tk.Label(master, text="", font=("Courier", 14))
        self.hangman_label.pack(pady=10)

        self.word_label = tk.Label(master, text="", font=("Arial", 24))
        self.word_label.pack(pady=10)

        self.input_entry = tk.Entry(master, font=("Arial", 18))
        self.input_entry.pack()

        self.submit_button = tk.Button(master, text="Guess", command=self.make_guess)
        self.submit_button.pack(pady=10)

        self.message_label = tk.Label(master, text="", font=("Arial", 14))
        self.message_label.pack(pady=10)

        self.tries_label = tk.Label(master, text="", font=("Arial", 14))
        self.tries_label.pack()

        self.new_game_button = tk.Button(master, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=10)

        self.new_game()

    def new_game(self):
        self.current_word = random.choice(self.words)
        self.guessed_letters = set()
        self.tries_left = self.max_tries
        self.update_word_display()
        self.update_hangman_display()
        self.message_label.config(text="")
        self.tries_label.config(text=f"Tries left: {self.tries_left}")
        self.input_entry.config(state="normal")
        self.submit_button.config(state="normal")

    def update_word_display(self):
        display = ""
        for letter in self.current_word:
            if letter in self.guessed_letters:
                display += letter
            else:
                display += "_"
        self.word_label.config(text=display)

    def update_hangman_display(self):
        self.hangman_label.config(text=self.hangman_stages[self.max_tries - self.tries_left])

    def make_guess(self):
        guess = self.input_entry.get().lower()
        self.input_entry.delete(0, tk.END)

        if len(guess) != 1:
            self.message_label.config(text="Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            self.message_label.config(text="You already guessed that letter.")
            return

        self.guessed_letters.add(guess)

        if guess in self.current_word:
            self.message_label.config(text="Good guess!")
        else:
            self.tries_left -= 1
            self.message_label.config(text="Incorrect guess.")
            self.update_hangman_display()

        self.update_word_display()
        self.tries_label.config(text=f"Tries left: {self.tries_left}")

        if "_" not in self.word_label.cget("text"):
            self.message_label.config(text="Congratulations! You won!")
            self.input_entry.config(state="disabled")
            self.submit_button.config(state="disabled")
        elif self.tries_left == 0:
            self.message_label.config(text=f"Game over. The word was: {self.current_word}")
            self.input_entry.config(state="disabled")
            self.submit_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()