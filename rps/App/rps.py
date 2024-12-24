import random
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk

helpstring = '''Usage:
\trps.py [options] [choice]

Example:2
\t rps.py scissors

Options:
\tMETA OPTIONS
\t\t-h or --help
\t\t\tPrints a help message
\t\t-c or --credits
\t\t\tShows creators of rps.py and its associated custom modules

\tFUNCTIONAL OPTIONS
\t\t-s or --seed
\t\t\tSet a custom seed for the computer's RNG.
'''


def translate(x):
    if x == 0:
        return 'Rock'
    elif x == 1:
        return 'Paper'
    elif x == 2:
        return 'Scissors'


def simulate_game(x, y):
    if x == y:
        return 'tie'
    elif (x == 0 and y == 1) or \
            (x == 1 and y == 2) or \
            (x == 2 and y == 0):
        return 'comp_win'
    else:
        return 'user_win'


def result_message(user_choice, comp_choice, result):
    if result == 'user_win':
        print(f'You won! You went {translate(user_choice)}, while the computer went {translate(comp_choice)}.')
    elif result == 'comp_win':
        print(f'You lost! You went {translate(user_choice)}, while the computer went {translate(comp_choice)}.')
    else:
        print(f'It was a tie! Both you and the computer went for {translate(comp_choice)}.')


# globals
user_win = 0
number_tie = 0
total_game = 0
comp_win = 0


def quit_application():
    global total_game, user_win, number_tie, comp_win
    if total_game == 0:
        print("Let's play next time!")
    else:
        user_win_rate = user_win / (total_game - number_tie) if (total_game - number_tie) > 0 else 0
        print(f"You won {user_win} times, tied {number_tie} times, and lost {comp_win} times!")
        print(f'Games played: {total_game}')
        print('Quitting...')
        if 'root' in globals():
            root.destroy()

def start_gui():
    global root
    root = tk.Tk()
    root.title("Rock Paper Scissors")

    button_counters = {"rock": 0, "paper": 0, "scissors": 0}

    def button_clicked(choice):
        global user_win, number_tie, total_game, comp_win
        button_counters[choice] += 1
        counter_label[choice].config(text=f'{choice.capitalize()} clicked: {button_counters[choice]}x')

        user_choice = {"rock": 0, "paper": 1, "scissors": 2}[choice]
        comp_choice = random.randint(0, 2)
        result = simulate_game(user_choice, comp_choice)
        result_message(user_choice, comp_choice, result)
        total_game += 1
        if result == 'user_win':
            user_win += 1
        elif result == 'tie':
            number_tie += 1
        elif result == 'comp_win':
            comp_win += 1
        messagebox.showinfo("Game Result",
                            f"You chose {translate(user_choice)}!\nComputer chose {translate(comp_choice)}.\n{result.capitalize()}")

    frame = tk.Frame(root)
    frame.pack(pady=40)

    counter_label = {}
    image = {}  # Initialize image dictionary
    for choice in ["rock", "paper", "scissors"]:
        try:
            # Updated image path to use os.path.join to handle different operating systems
            image_path = os.path.join(os.path.dirname(__file__), f"{choice}.png")
            image[choice] = PhotoImage(file=image_path)
            button = tk.Button(frame, text=choice.capitalize(), image=image[choice],
                                command=lambda ch=choice: button_clicked(ch))
            button.pack(side=tk.LEFT, padx=10)
        except tk.TclError:
            # If image fails to load, create a button with no image
            button = tk.Button(
                frame,
                text=choice.capitalize(),
                command=lambda ch=choice: button_clicked(ch)
            )
            button.pack(side=tk.LEFT, padx=10)
            print(f"Warning: Failed to load image for {choice}. Using text-only button.")

        counter_label[choice] = tk.Label(root, text=f'{choice.capitalize()}: 0')
        counter_label[choice].pack()

    quit_button = tk.Button(frame, text='Quit', command=quit_application)
    quit_button.pack(pady=5)
    root.mainloop()

def start_text_mode():
    user_win = 0
    number_tie = 0
    total_game = 0
    comp_win = 0

    s_user_input = None
    user_final = None

    #  while s_user_input not in quit_strings:
    while True:
        validity = False
        comp_choice = random.randint(0, 2)  # LCD -- 0 = rock, 1 = paper, 2 = scissors
        print('Rock, paper, or scissors? ("quit" to exit)')
        user_input = input('Choice: ')
        s_user_input = user_input.lower().replace(" ", "")

        if s_user_input in ['quit', 'exit', 'q']:
            quit_application()
            break
        elif 'rock' in s_user_input:
            if 'scissor' in s_user_input or 'paper' in s_user_input:
                print('Choose one only!\n')
            else:
                user_final = 0
                validity = True
        elif 'paper' in s_user_input:
            if 'scissor' in s_user_input or 'rock' in s_user_input:
                print('Choose one only!\n')
            else:
                user_final = 1
                validity = True
        elif 'scissor' in s_user_input:
            if 'rock' in s_user_input or 'paper' in s_user_input:
                print('Choose one only!\n')
            else:
                user_final = 2
                validity = True

        if validity:
            total_game += 1
            result = simulate_game(user_final, comp_choice)
            result_message(user_final, comp_choice, result)
            if result == 'user_win':
                user_win += 1
            elif result == 'tie':
                number_tie += 1
            elif result == 'comp_win':
                comp_win += 1
            print(f"You've won {user_win} times, tied {number_tie} times, and lost {comp_win} times!")
            print(f'Games played: {total_game}\n')


if __name__ == '__main__':

    if len(sys.argv) > 1:
        validity = True
        user_final = None
        meta_mode = False  # LCD -- "meta_mode" is enabled when you use an argument that's not meant to have a functional output, like -h or -c.

        help_args = {'--help', '-help', '-h', '-?', '--h'}
        broad_args = {'--help', '-help', '-h', '-?', '--h', '-c', '--credits', '-s',
                      '--seed'}  # LCD -- i dont think this is the "right way" to do this
        for i in sys.argv:
            if i in help_args:
                print(helpstring)
                meta_mode = True  # LCD -- meta_mode enabled because -h was ran
            elif (i == '-c') or (i == '--credits'):
                credits = ('Leo Dean', 'Linh Pham')
                print(f'Rock Paper Scissors IT111 final by {credits[0]} & {credits[1]}.\n')
                meta_mode = True  # LCD -- meta_mode enabled because -c was ran
            elif (i == '-s') or (i == '--seed'):
                try:
                    random.seed(sys.argv[sys.argv.index(i) + 1])  # LCD -- lol
                except IndexError:
                    print("Error: Seed value not provided after -s/--seed option.")
                    validity = False
                    meta_mode = True
                except ValueError:
                    print("Error: Invalid seed value.")
                    validity = False
                    meta_mode = True

        if not meta_mode and validity:
            comp_choice = random.randint(0, 2)
            s_user_input = sys.argv[-1].lower().replace(" ", "")
            if 'rock' in s_user_input:
                user_final = 0
            elif 'paper' in s_user_input:
                user_final = 1
            elif 'scissor' in s_user_input:
                user_final = 2
            elif sys.argv[-1] not in broad_args:
                print(f'"{sys.argv[-1]}" is not a valid choice!\n')
                validity = False

            if validity:
                total_game += 1
                result = simulate_game(user_final, comp_choice)
                result_message(user_final, comp_choice, result)
                if result == 'user_win':
                    user_win += 1
                elif result == 'tie':
                    number_tie += 1
                elif result == 'comp_win':
                    comp_win += 1

                print('')
    else:

        print("Welcome to Rock, Paper, Scissors!")
        print("Choose your game mode:")
        print("1. Text-Based Mode")
        print("2. GUI Mode")

        while True:
            choice = input("Enter your choice (1 or 2): ")
            if choice == '1':
                start_text_mode()
                break
            elif choice == '2':
                start_gui()
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
